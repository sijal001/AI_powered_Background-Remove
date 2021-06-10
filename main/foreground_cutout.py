# import modules to handle files
import os
import glob
import shutil
from PIL import Image

# import modules to train models
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import pandas as pd
import numpy as np

def process_image(image_path):
    """
    Function to process image into the input format required
    for model
    """

    # read image
    im = Image.open(image_path)


    # define image to tensor transform
    im_transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    # unify image channels to 3
    im = np.asarray(im)
    if len(im.shape) == 2:
        im = im[:, :, None]
    if im.shape[2] == 1:
        im = np.repeat(im, 3, axis=2)
    elif im.shape[2] == 4:
        im = im[:, :, 0:3]

    # convert image to PyTorch tensor
    im = Image.fromarray(im)
    im = im_transform(im)#.cuda()

    # add mini-batch dim
    im = im[None, :, :, :]

    # resize image for input
    im_b, im_c, im_h, im_w = im.shape
    ref_size = 512
    if max(im_h, im_w) < ref_size or min(im_h, im_w) > ref_size:
        if im_w >= im_h:
            im_rh = ref_size
            im_rw = int(im_w / im_h * ref_size)
        elif im_w < im_h:
            im_rw = ref_size
            im_rh = int(im_h / im_w * ref_size)
    else:
        im_rh = im_h
        im_rw = im_w

    im_rw = im_rw - im_rw % 32
    im_rh = im_rh - im_rh % 32
    im = F.interpolate(im, size=(im_rh, im_rw), mode='area')

    return im

def cut_out(image, matte) -> tuple:
    """
    Function to visualize results

    returns: tuple of images:
    * image cutout
    * image combining original image, image cutout, predicted alpha matte
    """
    # calculate display resolution
    print(image.shape)
    h, w = image.shape[0], image.shape[1]
    rw, rh = 800, int(h * 800 / (3 * w))

    # obtain predicted foreground
    image = np.asarray(image)
    if len(image.shape) == 2:
        image = image[:, :, None]
    if image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
    elif image.shape[2] == 4:
        image = image[:, :, 0:3]
        
    matte = np.repeat(np.asarray(matte)[:, :, None], 3, axis=2) / 255
    foreground = image * matte + np.full(image.shape, 255) * (1 - matte)
    Image.fromarray(((foreground).astype('uint8'))).save(os.path.join("./static/bgrm_result", "result.png"))
    foreground = Image.fromarray(np.uint8(foreground))

    return  foreground