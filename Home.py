import numpy as np
import streamlit as st
from tensorflow.keras import Sequential , layers
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from PIL import Image
st.set_page_config(
    page_title="Smart Skincare Recommender",
    page_icon= "💅" ,
    layout="centered",
    initial_sidebar_state="expanded",
)
# ------------------------- Load keras model ----------------------
classes = ['blackhead','comedonical-acne','eczema','pustule-acne','rosacea', 'wrinkle']
@st.cache_resource
def load_prediction_model():
    base_model = MobileNetV2(
        input_shape=(300, 300, 3), include_top=False, weights=None
    )

    model = Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(64, activation='relu'),
        layers.Dense(len(classes), activation='sigmoid'),
    ])
    model.load_weights('model_weights.weights.h5')
    return model

model = load_prediction_model()
def predict_skin_condition(uploaded_image, model , threshold = 0.4):
    size = (300 , 300)
    image = Image.open(uploaded_image)
    image = image.resize(size)
    img_array = np.asarray(image)

    normalized_image_array = img_array.astype(np.float32) / 255.0
    data = np.expand_dims(normalized_image_array, axis=0)

    predictions = model.predict(data)[0]
    detected_conditions = []
    for i, prob in enumerate(predictions):
        if prob >= threshold:
            detected_conditions.append(
                {"condition": classes[i], "confidence": float(prob)}
            )

    return detected_conditions
# -----------------------------------------------------------------
st.title("Smart Skincare Recommender")
st.write("✨ Your personalized guide to finding the right solutions for your skin concerns ✨")
img = Image.open("image.jpeg")
st.image(img, caption="Understand your skin, Discover your glow." , use_container_width=True)

# upload photo to detect problems
st.divider()
col1 , col2 = st.columns(2)
with col1:
    username = st.text_input("Full Name" , placeholder="Omnia Emad")
    age = st.number_input("Age" ,value=20)
    skin_type = st.radio(
        "Skin Type",
        ['Dry' ,'Normal','Combined', 'Oily']
    )
with col2:
    uploaded_image = st.file_uploader("Upload your image", type=["jpg", "png", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded image", width=450)


_, col_center, _ = st.columns([1, 2, 1])
with col_center:
    submit = st.button('Abracadabra… bad skin, disappear! 🪄', type="primary", use_container_width=True)

if submit:
    if uploaded_image is None:
        st.warning("⚠️ Please upload a skin photo first!")
    else:
        with st.spinner("Analyzing skin conditions... 🔮"):
            detected_conditions = predict_skin_condition(uploaded_image, model)
            result = []
            st.balloons()
            st.subheader("🔍 Detected Skin Features:")
            st.session_state['user_name'] = username
            st.session_state['skin_type'] = skin_type
            st.session_state['analysis_done'] = True
            if not detected_conditions:
                st.write("Wow!..You have a pure skin!")
            else:
                for condition in detected_conditions:
                    cond_name = condition["condition"]
                    conf_score = condition["confidence"]
                    result.append(cond_name)
                    col_name, col_bar = st.columns([1, 2])
                    with col_name:
                        st.write(f"**{cond_name.replace('-', ' ').title()}**")
                    with col_bar:
                        st.progress(conf_score, text=f"{round(conf_score * 100, 1)}%")
            st.session_state['user_problems'] = result
# ------------------------ Recommendation products --------------------------
if st.session_state.get('analysis_done', False):
    st.divider()
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        clicked = st.button(
            "Show Recommended Products 🛍️ ➡",
            type="primary",
            use_container_width=True,
        )
        if clicked:
            st.switch_page("pages/Recommendation.py")
# ------------------------ About the developer section -----------------------
st.divider()
col1 , col2 = st.columns([1.3 , 1] , gap='medium')
with col1:
    st.subheader('About The Developer👩🏻‍💻')
    st.markdown('''
    ***Hi, I’m Omnia!***\n
    I’m an AI student passionate about Data Analysis, Machine Learning, and building intelligent solutions
    that turn data into meaningful insights.
    This project combines my interest in AI, skincare,
    and data-driven decision making to create a more personalized and insightful skincare experience.💗''')
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(
    """
    🔗 **Connect with me:** 
    [LinkedIn](https://www.linkedin.com/in/omnia-emad-8599a6327) | 
    [Kaggle](https://www.kaggle.com/omniaemad12) | 
    [Resume](https://drive.google.com/file/d/1Va5j9xm11Bhs_Pqeh-r7b0PxVlpnWzR8/view?usp=sharing)
    """
    )

with col2:
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    img = Image.open("Screenshot 2026-08-13 030615.png")
    st.image(img, caption="LinkedIn profile", use_container_width=True)


## ----------------------- Gemini Suggestions -------------------
st.markdown("""
    <style>
    /* 1. خلفية الصفحة الرئيسية هادية وكريمي */
    .stApp {
        background-color: #FCF8F8 !important;
    }

    /* 2. خلفية الـ Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F4DADA !important;
    }

    /* 3. العناوين الرئيسية والفرعية */
    h1, h2, h3 {
        color: #B2535B !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 4. حقول الإدخال (Text input & Number input) */
    div[data-baseweb="input"] > div {
        background-color: #F4DADA !important;
        border-radius: 10px !important;
        border: 1.5px solid #E6D2C8 !important;
        color: #2B2D42 !important;
    }

    /* تغيير لون الحدود لما تضغطي جوه الحقل */
    div[data-baseweb="input"] > div:focus-within {
        border-color: #D9777F !important;
        box-shadow: 0 0 6px rgba(217, 119, 127, 0.25) !important;
    }

    /* 5. صندوق رفع الملفات (File Uploader) */
    [data-testid="stFileUploadDropzone"] {
        background-color: #F4DADA !important;
        border: 2px dashed #D9777F !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }

    /* زرار Browse files اللي جوه File Uploader */
    [data-testid="stFileUploadDropzone"] button {
        background-color: #F4DADA !important;
        color: #B2535B !important;
        border: 1px solid #D9777F !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploadDropzone"] button:hover {
        background-color: #F4DADA !important;
        color: white !important;
    }



/* 2. تنسيق شكل الزرار نفسه */
div.stButton > button {
    background-color: #F4DADA !important;
    color: #5C2C30 !important; /* لون خط غامق عشان يقرأ بوضوح فوق الوردي الفاتح */
    border-radius: 12px !important;
    border: 1px solid #E6B8B8 !important; /* بوردر خفيف يبرز شكله */
    font-weight: bold !important;
    padding: 0.65rem 1.5rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 10px rgba(217, 119, 127, 0.15) !important;
}

    /* تأثير الماوس (Hover) على الزرار */
    div.stButton > button:hover {
        background-color: #F4DADA !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 14px rgba(217, 119, 127, 0.35) !important;
    }

    /* 7. تظبيط الـ Radio Buttons */
    div[role="radiogroup"] {
        background-color: #F4DADA;
        padding: 10px;
        border-radius: 10px;
        border: 1.5px solid #E6D2C8;
    }

    /* 8. الخطوط الفاصلة (Divider) */
    hr {
        border-color: #E6D2C8 !important;
    }
    </style>
    
""", unsafe_allow_html=True)