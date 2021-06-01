# Remove_Image_Background

Project status : work in progress
 
## Table of Contents
 
- [Introduction](#introduction)
 
- [Installation](#installation)
 
- [Data sources](#data-sources)
 
- [Instructions](#instructions)
 
- [Architecture](#architecture)
 
---
 
## Introduction
### Description
Written in AI, this is an AI-powered background removal service project for *Faktion* & *BeCode*.

 
### Objectives
- Use computer vision techniques to remove the background from a still 2D image.
- Exploration of pre-trained models for image background removal.
- (Optional) Deployment of model for end-customers.
 
### When?
This is a 2 week project; to be completed by `11/06/2021`.
 
 
## Installation
To run the program and see a live demo of the code, you need:
- To install the libraries below
 
### Install the libraries
| Library          | Used to                                        |
| ---------------- | :----------------------------------------------|
| Numpy            | To handle Numpy arrays                         |
| Pandas           | To store and access info in a DataFrame        |
| Matplotlib       | To plot the data                               |
| OpenCV           | To read, modify, generate image & video        |
| jupyter          | To open Jupyter Notebook                       |
| TensorFlow       | To make use of the Keras framework             |
| pillow           | To work with images                            |
| h5py             | To save and load models                        |
 
 
 
 
 
Follow these instructions to install the required libraries: on terminal
1. Open your terminal;
2. cd to the directory where the `requirements.txt` file is located;
3. Create and activate your virtual environment.
4. Run the command:
```pip install -r requirements.txt```
 
### Additional info
Note that we develop the source code on
- macOS Big Sur
- Windows 10
 
## Data Sources
To train our machine learning model, we use the [DUTS Image Dataset](http://saliencydetection.net/duts/):
As at June 2021, this is the largest saliency detection benchmark. It comprises of
* 10,553 training images
* and 5,019 test images

References:
Lijun Wang, Huchuan Lu, Yifan Wang , Mengyang Feng, Dong Wang, Baocai Yin, Xiang Ruan, "Learning to Detect Salient Objects with Image-level Supervision", CVPR2017
 
 
## Instructions
### How to run the program


 
## Architecture
The project is structured as follows:
 
```
Remove_Image_Background
│   README.md               :explains the project
│   requirements.txt        :packages to install to run the program
│   .gitignore              :specifies files & directories to exclude from GitHub
│   main.py                 :script to run in order to start the program
│
└───core                    :contains all the core scripts of the program
│   │   __init__.py
│   │
│   └───assets              
│       ├───data
│       ├───images
│       └───models
``` 
### Usage example
![Example input](assets/images/example_input.jpeg)
![Example output](assets/images/example_output.png)
 
 
### Roadmap
- [x] Explore dataset
- [ ] Review literature on background removal techniques
- [ ] Model implementation
- [ ] Evaluate model performance
- [ ] Model deployment
 
 
### Author(s) and acknowledgment
This project is carried out by:
- **[Derrick Van Frausum](https://github.com/DerrickDDInAI)**
- **[Joren Vervoort](https://github.com/Joren-Vervoort)**
- **[Sijal Joshi](https://github.com/sijal001)**
 
from Theano 2.27 promotion at [BeCode](https://becode.org).
 
 
 
 
We would like to thank:
- [Faktion](https://www.faktion.com/) for the opportunity to work on this use-case
- Lijun Wang, Huchuan Lu, Yifan Wang ,Mengyang Feng, Dong Wang, Baocai Yin, Xiang Ruan for the *DUTS* dataset
- and our colleagues and coaches at [BeCode](https://becode.org) for their help and guidance.
