# PlantCare AI

PlantCare AI is a plant disease detection project built to help identify common plant diseases from leaf images. The app allows users to upload a picture of a plant leaf, runs it through a trained deep learning model, and shows the predicted disease along with a basic treatment and prevention guide.

This project is useful for farmers, gardeners, students, and anyone who wants a quick way to check whether a plant looks healthy or shows signs of disease.

## Overview

Plant diseases can spread quickly and often damage crops before they are noticed. Early detection helps reduce losses and makes treatment more effective. This project uses image recognition to classify plant leaves into healthy and diseased categories.

The application is built with Python and Streamlit, and the prediction model is based on a convolutional neural network trained on plant image data.

## Features

- Upload a plant leaf image
- Detect disease using a trained deep learning model
- Display plant type and predicted disease
- Show confidence score of the prediction
- Provide symptom, chemical, organic, and prevention guidance
- Simple and user-friendly web interface

## How it works

1. The user uploads an image of a plant leaf.
2. The app preprocesses the image to the required size and format.
3. The model predicts the class of the image.
4. The result is displayed with the plant name, disease name, and confidence level.
5. The app shows recommended treatment and prevention steps based on the detected disease.

## Supported crops and diseases

The model has been trained on a wide range of plant categories, including:

- Apple
- Blueberry
- Cherry
- Corn
- Grape
- Orange
- Peach
- Pepper
- Potato
- Raspberry
- Soybean
- Squash
- Strawberry
- Tomato

The dataset includes both healthy and diseased leaf samples for many of these crops.

## Tech Stack

- Python
- Streamlit
- TensorFlow / Keras
- NumPy
- PIL / image preprocessing
- Deep learning model for image classification
