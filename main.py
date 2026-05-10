import streamlit as st
import numpy as np
import keras

# =========================
# Custom CSS for Beautiful UI
# =========================
st.markdown("""
<style>
    /* Overall app styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4CAF50 0%, #45a049 100%);
        color: white;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFD700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-family: 'Arial Black', sans-serif;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* File uploader */
    .uploadedFile {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed #FFD700;
    }
    
    /* Success, warning, info boxes */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Cards for results */
    .result-card {
        background: rgba(255,255,255,0.95);
        color: #333;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-left: 5px solid #4CAF50;
    }
    
    /* Home page image */
    .home-image {
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        margin: 20px 0;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #E8F5E8;
    }
    
    /* Selectbox */
    .stSelectbox {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Disease Remedy Dictionary
# =========================
disease_info = {

# ================= APPLE =================
'Apple___Apple_scab': {
    "Symptoms": "Olive-green spots on leaves and fruits.",
    "Chemical Control": "Spray Captan or Myclobutanil.",
    "Organic Control": "Use sulfur-based fungicides.",
    "Fertilizer": "Balanced NPK with compost.",
    "Prevention": "Remove fallen leaves, ensure airflow."
},

'Apple___Black_rot': {
    "Symptoms": "Brown lesions on leaves, black rotten fruits.",
    "Chemical Control": "Use Mancozeb or Thiophanate-methyl.",
    "Organic Control": "Copper fungicide sprays.",
    "Fertilizer": "Add potassium-rich fertilizer.",
    "Prevention": "Prune infected parts."
},

'Apple___Cedar_apple_rust': {
    "Symptoms": "Yellow-orange spots on leaves.",
    "Chemical Control": "Use Myclobutanil fungicide.",
    "Organic Control": "Neem oil spray.",
    "Fertilizer": "Balanced NPK.",
    "Prevention": "Remove nearby cedar trees."
},

'Apple___healthy': {
    "Symptoms": "No disease.",
    "Chemical Control": "Not required.",
    "Organic Control": "Maintain soil health.",
    "Fertilizer": "Compost + NPK (10-10-10).",
    "Prevention": "Regular monitoring."
},

# ================= BLUEBERRY =================
'Blueberry___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "Not required.",
    "Organic Control": "Maintain acidic soil (pH 4.5–5.5).",
    "Fertilizer": "Ammonium sulfate fertilizer.",
    "Prevention": "Proper irrigation."
},

# ================= CHERRY =================
'Cherry_(including_sour)___Powdery_mildew': {
    "Symptoms": "White powder on leaves.",
    "Chemical Control": "Use Sulfur or Potassium bicarbonate.",
    "Organic Control": "Neem oil spray.",
    "Fertilizer": "Balanced NPK.",
    "Prevention": "Improve airflow."
},

'Cherry_(including_sour)___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "Not required.",
    "Organic Control": "Proper pruning.",
    "Fertilizer": "Compost.",
    "Prevention": "Maintain spacing."
},

# ================= CORN =================
'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
    "Symptoms": "Gray rectangular lesions.",
    "Chemical Control": "Use Azoxystrobin or Mancozeb.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Nitrogen balanced.",
    "Prevention": "Crop rotation."
},

'Corn_(maize)___Common_rust_': {
    "Symptoms": "Reddish pustules.",
    "Chemical Control": "Propiconazole fungicide.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Avoid excess nitrogen.",
    "Prevention": "Resistant hybrids."
},

'Corn_(maize)___Northern_Leaf_Blight': {
    "Symptoms": "Long gray-green lesions.",
    "Chemical Control": "Mancozeb or Azoxystrobin.",
    "Organic Control": "Crop rotation.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Use resistant seeds."
},

'Corn_(maize)___healthy': {
    "Symptoms": "Healthy crop.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain soil health.",
    "Fertilizer": "NPK fertilizer.",
    "Prevention": "Proper irrigation."
},

# ================= GRAPE =================
'Grape___Black_rot': {
    "Symptoms": "Black spots on leaves and fruits.",
    "Chemical Control": "Mancozeb or Myclobutanil.",
    "Organic Control": "Copper fungicide.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Remove infected fruits."
},

'Grape___Esca_(Black_Measles)': {
    "Symptoms": "Leaf discoloration and fruit spotting.",
    "Chemical Control": "No effective cure.",
    "Organic Control": "Remove infected vines.",
    "Fertilizer": "Balanced fertilizer.",
    "Prevention": "Avoid pruning wounds."
},

'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
    "Symptoms": "Brown spots on leaves.",
    "Chemical Control": "Mancozeb spray.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Prune properly."
},

'Grape___healthy': {
    "Symptoms": "Healthy vine.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain vineyard hygiene.",
    "Fertilizer": "NPK fertilizer.",
    "Prevention": "Proper pruning."
},

# ================= ORANGE =================
'Orange___Haunglongbing_(Citrus_greening)': {
    "Symptoms": "Yellow shoots, misshapen fruits.",
    "Chemical Control": "Control psyllids using Imidacloprid.",
    "Organic Control": "Neem oil for vector control.",
    "Fertilizer": "Micronutrients (Zn, Fe).",
    "Prevention": "Remove infected trees."
},

# ================= PEACH =================
'Peach___Bacterial_spot': {
    "Symptoms": "Dark lesions on leaves.",
    "Chemical Control": "Copper bactericides.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Potassium-rich fertilizer.",
    "Prevention": "Use resistant varieties."
},

'Peach___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain orchard hygiene.",
    "Fertilizer": "Balanced NPK.",
    "Prevention": "Proper irrigation."
},

# ================= PEPPER =================
'Pepper,_bell___Bacterial_spot': {
    "Symptoms": "Small dark spots.",
    "Chemical Control": "Copper sprays.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Potassium-rich.",
    "Prevention": "Avoid overhead watering."
},

'Pepper,_bell___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Good soil care.",
    "Fertilizer": "NPK.",
    "Prevention": "Proper spacing."
},

# ================= POTATO =================
'Potato___Early_blight': {
    "Symptoms": "Dark concentric spots.",
    "Chemical Control": "Mancozeb.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Add phosphorus & potassium.",
    "Prevention": "Crop rotation."
},

'Potato___Late_blight': {
    "Symptoms": "Water-soaked lesions.",
    "Chemical Control": "Metalaxyl + Mancozeb.",
    "Organic Control": "Copper fungicide.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Destroy infected plants."
},

'Potato___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Soil health maintenance.",
    "Fertilizer": "NPK.",
    "Prevention": "Regular monitoring."
},

# ================= OTHER =================
'Raspberry___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain pruning.",
    "Fertilizer": "Compost.",
    "Prevention": "Proper care."
},

'Soybean___healthy': {
    "Symptoms": "Healthy crop.",
    "Chemical Control": "None.",
    "Organic Control": "Soil fertility.",
    "Fertilizer": "Nitrogen fixation support.",
    "Prevention": "Crop rotation."
},

'Squash___Powdery_mildew': {
    "Symptoms": "White powdery coating.",
    "Chemical Control": "Sulfur fungicide.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Air circulation."
},

'Strawberry___Leaf_scorch': {
    "Symptoms": "Red/purple leaf edges.",
    "Chemical Control": "Fungicide sprays.",
    "Organic Control": "Remove infected leaves.",
    "Fertilizer": "Balanced NPK.",
    "Prevention": "Avoid overcrowding."
},

'Strawberry___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Good irrigation.",
    "Fertilizer": "Compost.",
    "Prevention": "Regular care."
},

# ================= TOMATO =================
'Tomato___Bacterial_spot': {
    "Symptoms": "Dark leaf spots.",
    "Chemical Control": "Copper bactericide.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Potassium-rich.",
    "Prevention": "Avoid wet leaves."
},

'Tomato___Early_blight': {
    "Symptoms": "Brown rings on leaves.",
    "Chemical Control": "Mancozeb.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Add potassium.",
    "Prevention": "Crop rotation."
},

'Tomato___Late_blight': {
    "Symptoms": "Dark lesions.",
    "Chemical Control": "Metalaxyl.",
    "Organic Control": "Copper spray.",
    "Fertilizer": "Balanced nutrients.",
    "Prevention": "Remove infected plants."
},

'Tomato___Leaf_Mold': {
    "Symptoms": "Yellow spots, mold underside.",
    "Chemical Control": "Chlorothalonil.",
    "Organic Control": "Improve airflow.",
    "Fertilizer": "Balanced.",
    "Prevention": "Reduce humidity."
},

'Tomato___Septoria_leaf_spot': {
    "Symptoms": "Small circular spots.",
    "Chemical Control": "Mancozeb.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced.",
    "Prevention": "Remove infected leaves."
},

'Tomato___Spider_mites Two-spotted_spider_mite': {
    "Symptoms": "Yellow specks, webbing.",
    "Chemical Control": "Abamectin.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced.",
    "Prevention": "Maintain humidity."
},

'Tomato___Target_Spot': {
    "Symptoms": "Circular spots with rings.",
    "Chemical Control": "Chlorothalonil.",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Balanced.",
    "Prevention": "Remove debris."
},

'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
    "Symptoms": "Yellow curled leaves.",
    "Chemical Control": "Control whiteflies (Imidacloprid).",
    "Organic Control": "Neem oil.",
    "Fertilizer": "Micronutrients.",
    "Prevention": "Remove infected plants."
},

'Tomato___Tomato_mosaic_virus': {
    "Symptoms": "Mosaic leaf pattern.",
    "Chemical Control": "No cure.",
    "Organic Control": "Remove infected plants.",
    "Fertilizer": "Balanced.",
    "Prevention": "Sanitize tools."
},

'Tomato___healthy': {
    "Symptoms": "Healthy plant.",
    "Chemical Control": "None.",
    "Organic Control": "Maintain soil health.",
    "Fertilizer": "NPK (10-10-10).",
    "Prevention": "Regular monitoring."
}
}

# =========================
# Model Prediction Function
# =========================
def model_prediction(test_image):
    model = keras.models.load_model("fixed_plant_disease_model.keras")

    image = keras.preprocessing.image.load_img(test_image, target_size=(128,128))
    input_arr = keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])

    predictions = model.predict(input_arr)

    result_index = np.argmax(predictions)
    confidence = np.max(predictions) * 100

    return result_index, confidence


# =========================
# Sidebar
# =========================
st.sidebar.markdown("""
<div style="text-align: center; padding: 20px;">
    <h2 style="color: #FFD700; margin-bottom: 30px;">🌿 PlantCare AI</h2>
    <p style="color: #E8F5E8; font-size: 14px;">Advanced Disease Detection System</p>
</div>
""", unsafe_allow_html=True)

app_mode = st.sidebar.selectbox(
    "🌟 Choose Your Path",
    ["🏠 Home", "ℹ️ About", "🔍 Disease Recognition"],
    help="Navigate through different sections of the app"
)


# =========================
# Home Page
# =========================
if app_mode == "🏠 Home":
    # Hero section
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: rgba(255,255,255,0.1); border-radius: 25px; margin-bottom: 30px;">
        <h1 style="font-size: 3em; margin-bottom: 10px;">🌱 PLANT DISEASE RECOGNITION SYSTEM</h1>
        <p style="font-size: 1.2em; color: #E8F5E8;">AI-Powered Plant Health Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main image
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("home_page.jpeg", use_container_width=True, caption="Advanced Plant Disease Detection")
    
    # Feature cards
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; text-align: center; margin: 10px;">
            <h3>🔬 AI Detection</h3>
            <p>State-of-the-art CNN models for accurate disease identification</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; text-align: center; margin: 10px;">
            <h3>💊 Treatment Guide</h3>
            <p>Comprehensive remedies and preventive measures</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; text-align: center; margin: 10px;">
            <h3>📊 Confidence Score</h3>
            <p>Reliable prediction confidence for better decision making</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; padding: 30px; background: rgba(76, 175, 80, 0.2); border-radius: 20px; margin-top: 30px;">
        <h2 style="color: #FFD700;">Ready to Diagnose Your Plants?</h2>
        <p style="font-size: 1.1em;">Upload a leaf image and get instant results with treatment recommendations</p>
        <p style="font-size: 1.3em; font-weight: bold;">➡️ Go to Disease Recognition to begin!</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# About Page
# =========================
elif app_mode == "ℹ️ About":
    st.markdown("""
    <div style="text-align: center; padding: 30px; background: rgba(255,255,255,0.1); border-radius: 20px; margin-bottom: 30px;">
        <h1>About PlantCare AI</h1>
        <p style="font-size: 1.2em;">Understanding Our Technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 25px; border-radius: 15px; height: 300px;">
            <h3 style="color: #FFD700;">📊 Dataset Overview</h3>
            <ul style="color: #E8F5E8; font-size: 16px; line-height: 1.6;">
                <li><strong>87,000+</strong> high-quality images</li>
                <li><strong>38 different</strong> plant disease classes</li>
                <li><strong>14 plant species</strong> covered</li>
                <li>Comprehensive disease spectrum</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 25px; border-radius: 15px; height: 300px;">
            <h3 style="color: #FFD700;">📈 Data Split</h3>
            <div style="color: #E8F5E8; font-size: 16px; line-height: 1.8;">
                <p><strong>Training Set:</strong> 70,000+ images</p>
                <p><strong>Validation Set:</strong> 17,000+ images</p>
                <p><strong>Test Set:</strong> 33 benchmark images</p>
                <br>
                <p><strong>Technology:</strong> Convolutional Neural Networks</p>
                <p><strong>Accuracy:</strong> Industry-leading performance</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology section
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(76, 175, 80, 0.2); padding: 30px; border-radius: 20px; margin-top: 30px;">
        <h2 style="text-align: center; color: #FFD700;">🚀 Advanced AI Technology</h2>
        <p style="text-align: center; font-size: 1.1em; color: #E8F5E8;">
            Our system uses state-of-the-art Convolutional Neural Networks trained on extensive datasets 
            to provide accurate plant disease detection with detailed treatment recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# Disease Recognition Page
# =========================
elif app_mode == "🔍 Disease Recognition":
    st.markdown("""
    <div style="text-align: center; padding: 30px; background: rgba(255,255,255,0.1); border-radius: 20px; margin-bottom: 30px;">
        <h1>🔍 Plant Disease Analysis</h1>
        <p style="font-size: 1.2em;">Upload a leaf image for instant diagnosis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload section
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 25px; border-radius: 15px; margin-bottom: 20px;">
        <h3 style="color: #FFD700; text-align: center;">📤 Upload Your Plant Leaf Image</h3>
    </div>
    """, unsafe_allow_html=True)
    
    test_image = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of the plant leaf for best results"
    )

    if test_image is not None:
        # Image display section
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; text-align: center;">
                <h4 style="color: #333; margin-bottom: 15px;">📸 Uploaded Image</h4>
            </div>
            """, unsafe_allow_html=True)
            st.image(test_image, use_container_width=True, caption="Your uploaded leaf image")
        
        # Buttons section
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.write("")  # Spacer
        
        with col2:
            if st.button("🔮 Analyze Disease", use_container_width=True):
                with st.spinner("🧠 AI is analyzing your image..."):
                    import time
                    time.sleep(2)  # Simulate processing time
                    
                    # Class labels
                    class_name = [
                        'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                        'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
                        'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                        'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
                        'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
                        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
                        'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
                        'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
                        'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                        'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
                        'Strawberry___Leaf_scorch', 'Strawberry___healthy',
                        'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
                        'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
                        'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
                        'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                        'Tomato___healthy'
                    ]

                    # Prediction
                    result_index, confidence = model_prediction(test_image)
                    predicted_disease = class_name[result_index]

                    # Clean display
                    plant, disease = predicted_disease.split("___")

                    # Results section
                    st.markdown("---")
                    st.markdown("""
                    <div style="text-align: center; padding: 20px; background: rgba(76, 175, 80, 0.2); border-radius: 20px; margin-bottom: 30px;">
                        <h2 style="color: #FFD700;">🎯 Analysis Complete!</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Result cards
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="result-card">
                            <h4 style="color: #4CAF50; margin-bottom: 10px;">🌿 Plant Type</h4>
                            <h3 style="color: #333; margin: 0;">{plant.replace('_', ' ')}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        color = "#FF6B6B" if disease != "healthy" else "#4CAF50"
                        icon = "⚠️" if disease != "healthy" else "✅"
                        st.markdown(f"""
                        <div class="result-card">
                            <h4 style="color: {color}; margin-bottom: 10px;">{icon} Disease Status</h4>
                            <h3 style="color: #333; margin: 0;">{disease.replace('_', ' ')}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        confidence_color = "#4CAF50" if confidence > 80 else "#FF9800" if confidence > 60 else "#FF6B6B"
                        st.markdown(f"""
                        <div class="result-card">
                            <h4 style="color: {confidence_color}; margin-bottom: 10px;">📊 Confidence</h4>
                            <h2 style="color: #333; margin: 0; font-size: 2em;">{confidence:.1f}%</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Treatment section
                    if disease != "healthy":
                        st.markdown("""
                        <div style="background: rgba(255,193,7,0.2); padding: 25px; border-radius: 15px; margin-top: 30px; border-left: 5px solid #FFC107;">
                            <h3 style="color: #FF6B35;">💊 Treatment & Prevention Guide</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        remedy = disease_info.get(predicted_disease)
                        
                        if remedy:
                            cols = st.columns(2)
                            items = list(remedy.items())
                            
                            for i, (key, value) in enumerate(items):
                                with cols[i % 2]:
                                    st.markdown(f"""
                                    <div style="background: rgba(255,255,255,0.9); padding: 15px; border-radius: 10px; margin: 5px 0; color: #333;">
                                        <strong style="color: #4CAF50;">{key}:</strong><br>
                                        {value}
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info("Treatment information for this disease is being updated.")
                    else:
                        st.markdown("""
                        <div style="background: rgba(76, 175, 80, 0.2); padding: 25px; border-radius: 15px; margin-top: 30px; text-align: center;">
                            <h3 style="color: #4CAF50;">🎉 Great News!</h3>
                            <p style="font-size: 1.2em; color: #E8F5E8;">Your plant appears to be healthy. Keep up the good care!</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col3:
            st.write("")  # Spacer