## Introduction
Welcome to the Real-time Face Recognition System using the Local Binary Patterns Histograms (LBPH) algorithm. This repository showcases an approach to face detection and identification using local texture patterns. We merge OpenCV and Python, this model gives a practical understanding of computer vision techniques.

## Prerequisites
1. Make sure you have a functional Python environment installed.
   Install the required packages using the following command:

  `pip install opencv-python`

2. Make sure dlib is installed...you might need to build wheels for it manually by installing `dlib-19.22.99-cp39-cp39-win_amd64.whl`

3. You need to download the pre-trained face detector:`haarcascade_frontalface_default.xml`

4. Also, I faced a problem with the environment variables.
   Make sure that the installed python in PATH

## Usage
1. Clone or download this repository onto your local machine.
2. Navigate to the project directory.
3. Execute the main script using this command: `python main.py`

Alternatively, you can directly launch and run `main.py` through a Python interpreter.

## Understanding the LBPH Algorithm
LBPH (Local Binary Patterns Histograms) is a well known algorithm for face recognition:
- **Pixel Labeling:** LBPH involves comparing pixel intensities with their local neighbors, resulting in binary patterns.
- **Parameters Used:** The algorithm's effectiveness lies in four crucial parameters: 
  - **Radius:** Imagine drawing a circle around a dot - this circle's size is set by the radius. 
  - **Neighbors:** It's like asking friends for their opinions - we ask neighboring dots for their colors.
  - **Grid X:** Imagine a checkerboard - this tells the computer how many squares(pixels) to make from left to right.
  - **Grid Y:** It says how many squares(pixels) to make from top to bottom.
- **Training Phase:** The model learns from labeled facial images during the training process.
- **Recognition Phase:** For recognition, the model evaluates input patterns against learned ones and assigns corresponding labels.

- **Brightness and Contrast Controls:** I have used `alpha` and `beta` to control the contrast and brightness adjustments, respectively.
`cv2.convertScaleAbs()` is used to adjust the contrast and brightness of the image.



