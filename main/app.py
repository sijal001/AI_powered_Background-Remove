from flask import Flask,render_template,url_for,request
from werkzeug.utils import secure_filename
from PIL import Image

import foreground_cutout as bgrm
import torch.nn.functional as F
import pandas as pd 
import numpy as np
import base64
import shutil
import timeit
import torch
import gdown
import git
import sys
import io
import os

# Download U2Net, MODNet and models

# if repository not already in directory, clone it
if not os.path.exists('U-2-Net'):
    git.Git(os.getcwd()).clone("https://github.com/xuebinqin/U-2-Net.git")

# if repository not already in directory, clone it
if not os.path.exists('MODNet'):
    git.Git(os.getcwd()).clone("https://github.com/ZHKKKe/MODNet.git")

# create the folder to save model
if not os.path.exists(r'./U-2-Net/saved_models/u2net/'):
    os.mkdir(r'./U-2-Net/saved_models/u2net/')

# download U-2-net model 
if not os.path.isfile(r'./U-2-Net/saved_models/u2net/u2net.pth'):
    url = 'https://drive.google.com/uc?id=1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ'
    output = r'./U-2-Net/saved_models/u2net/u2net.pth'
    gdown.download(url, output, quiet=False)

# download modnet_mobilenetn2 model 
if not os.path.isfile(r'./MODNet/pretrained/mobilenetv2_human_seg.ckpt'):
    url = 'https://drive.google.com/uc?id=1gNJXQPUBBp2mbA4q1Giz5mzv3EpxR7lq'
    output = r'./MODNet/pretrained/mobilenetv2_human_seg.ckpt'
    gdown.download(url, output, quiet=False)


main_path = sys.path[0]
scnd_path = sys.path[0]+"\\MODNet"

os.chdir(scnd_path)
# import local modules
from MODNet.src.models.modnet import MODNet

# define device
device = "cuda" if torch.cuda.is_available() else "cpu"

# rebuild model with same architecture as in training
modnet = torch.nn.DataParallel(MODNet()).to(device)

os.chdir(main_path)
# load model's state_dict
state_dict = torch.load(
    './model_checkpoint/model_checkpoint.pth',
    map_location=torch.device(device) # map to device
    )

# load state_dict into the network (works only if model architecture is the same as checkpoint architecture)
modnet.load_state_dict(state_dict)


# create the folder to upload images
if not os.path.exists(r'./static/upload/'):
    os.mkdir(r'./static/upload/')

# create the folder to upload images
if not os.path.exists(r'./static/bgrm_result/'):
    os.mkdir(r'./static/bgrm_result/')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'./static/upload/'


# *******************
def result_image():
    # path to image
    
    image_path = f".\\static\\upload\\{os.listdir(r'./static/upload/')[0]}"

    # process image into correct input format for model
    im = bgrm.process_image(image_path)

    # predict alpha matte
    _, _, matte = modnet(im, True)

    # load image to get the original shape
    image = np.asarray(Image.open(image_path))
    print(image.shape)

    # resize alpha matte to the original shape
    im_h = image.shape[0]
    im_w = image.shape[1]
    matte = F.interpolate(matte, size=(im_h, im_w), mode='area')
    matte = matte[0][0].data.cpu().numpy()
    print(matte.shape)

    # save matte
    Image.fromarray(((matte * 255).astype('uint8')), mode='L').save(os.path.join("./static/bgrm_result", "matte.png"))

    # image cutout
    matte = np.asarray(Image.open("./static/bgrm_result/matte.png"))
    bgrm.cut_out(image, matte)

# ******************
"""
def result_image():
    image = os.listdir(r'./static/upload/')[0]
    dest = '.\\static\\bgrm_result\\{}'.format(image)
    shutil.copy2('.\\static\\upload\\{}'.format(image), dest)
    return(dest)
""" 

def clean_dir(path):
    dir = '.\\static\\{}\\'.format(path)
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # remove image from dir "bgrm_result"
        clean_dir("bgrm_result")
        return render_template("index.html")

    elif request.method == 'POST':
        file = request.files['file_upload']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result_image()

        result_path = "./static/bgrm_result/result.png"
        im = Image.open(result_path)
        data = io.BytesIO()
        im.save(data, result_path.split(".")[-1])
        print(data, result_path.split(".")[-1])
        encoded_img_data = base64.b64encode(data.getvalue())

        # remove image from dir "upload"
        clean_dir("upload")
        return render_template('result.html', bgrm_result=encoded_img_data.decode('utf-8'))

if __name__ == '__main__':
	app.run(debug=True)