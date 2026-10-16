# 🌿 PlantCare AI — Plant Disease Detection & Treatment System

> Detect plant diseases from leaf images using deep learning and explore relevant treatment and prevention guidance.

PlantCare AI is a Python-based web application that uses a Convolutional Neural Network (CNN) to classify plant leaf images into healthy or diseased categories. Built with TensorFlow, Keras, and Streamlit, it provides predictions, confidence scores, and disease-specific care recommendations.

## ✨ Features

- 🖼️ **Leaf Image Upload:** Upload plant leaf images for analysis.
- 🧠 **Deep Learning Classification:** Predict plant health and disease categories using a trained CNN model.
- 🌱 **Multi-Crop Support:** Supports 14 crop types and 38 plant health and disease categories.
- 📊 **Confidence Scores:** View the model's prediction confidence.
- 💊 **Treatment Guidance:** Access symptom descriptions, chemical and organic treatment suggestions, and prevention tips.
- 🌐 **Interactive Web App:** Simple interface built with Streamlit.

## 🏗️ How It Works

```text
       ┌─────────────────────┐
       │  Upload Leaf Image  │
       └──────────┬──────────┘
                  ↓
       ┌─────────────────────┐
       │ Image Preprocessing │
       └──────────┬──────────┘
                  ↓
       ┌─────────────────────┐
       │   Trained CNN Model │
       │  TensorFlow / Keras │
       └──────────┬──────────┘
                  ↓
       ┌─────────────────────┐
       │ Disease Prediction  │
       │ + Confidence Score  │
       └──────────┬──────────┘
                  ↓
       ┌─────────────────────┐
       │ Treatment &         │
       │ Prevention Guidance │
       └─────────────────────┘
```

## 🌾 Supported Crops

The model supports the following 14 crop types:

Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, and Tomato.

The classification dataset includes healthy and diseased leaf categories.

## 🛠️ Tech Stack

- **Language:** Python
- **Deep Learning:** TensorFlow, Keras, CNN
- **Web Framework:** Streamlit
- **Image Processing:** PIL / Pillow, NumPy
- **Dataset:** Plant disease image dataset used for model training

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd PlantCare-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Ensure the trained model file is available at the location expected by the application.

### 4. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## 🎯 Problem It Solves

Plant diseases can affect crop quality and agricultural productivity. PlantCare AI provides an accessible image-based screening tool to help users identify potential plant diseases and explore possible treatment options.
