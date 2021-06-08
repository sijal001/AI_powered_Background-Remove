from flask import Flask,render_template,url_for,request
import pandas as pd 
from werkzeug.utils import secure_filename
import timeit
import os
import shutil

from PIL import Image
import base64
import io

# create the folder to upload images
if not os.path.exists(r'./static/upload/'):
    os.mkdir(r'./static/upload/')

# create the folder to upload images
if not os.path.exists(r'./static/bgrm_result/'):
    os.mkdir(r'./static/bgrm_result/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'./static/upload/'

def result_image():
    image = os.listdir(r'./static/upload/')[0]
    dest = '.\\static\\bgrm_result\\{}'.format(image)
    shutil.copy2('.\\static\\upload\\{}'.format(image), dest)
    return(dest)

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
        result_path = result_image()

        im = Image.open(result_path)
        data = io.BytesIO()
        im.save(data, result_path.split(".")[-1])
        encoded_img_data = base64.b64encode(data.getvalue())

        # remove image from dir "upload"
        print(result_path)
        clean_dir("upload")
        return render_template('result.html', bgrm_result=encoded_img_data.decode('utf-8'))

if __name__ == '__main__':
	app.run(debug=True)
