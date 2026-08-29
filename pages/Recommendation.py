import streamlit as st
import pandas as pd
import gdown
import os
from recommendation_engine import get_recommendations , get_profile

@st.cache_data
def load_data():
    products_final = pd.read_csv('products_final.csv')
    return products_final

products_final = load_data()
st.set_page_config(
    page_title="Recommendations Products",
    page_icon='🌸',
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Recommendation Engine Based on user problems")
user_name = st.session_state.get('user_name' , 'Unknown')
skin_type = st.session_state.get('skin_type' , 'Normal')
user_problems = st.session_state.get('user_problems' , ['Pure Skin'] )

# ------------------- Get Recommendations ------------------
st.subheader("🛍️ Recommended Products Profiles:")
recommended_products = get_profile(user_problems)
for product in recommended_products.items():
    p_id = product[0]
    p_info = product[1]
    with st.container(border=True):
        st.markdown(f"### 🧴 {p_info['product_name']}")

        col1, col2, col3 , col4 = st.columns(4)
        # Primary actives
        with col1:
            st.markdown("🎯 **Primary Actives:**")
            if p_info["primary_ings"]:
                for ing in p_info["primary_ings"]:
                    st.markdown(f"- :green[{ing}] 🌟")
            else:
                st.caption("None targeted directly")

        # Supportive Ingredients
        with col2:
            st.markdown("🤝 **Supportive:**")
            if p_info["supportive_ings"]:
                for ing in p_info["supportive_ings"]:
                    st.markdown(f"- :blue[{ing}] 💧")
            else:
                st.caption("None")

        # Irritants Alert
        with col3:
            st.markdown("⚠️ **Potential Irritants:**")
            if p_info["irr_ings"]:
                for ing in p_info["irr_ings"]:
                    st.markdown(f"- :red[{ing}] ⚡")
            else:
                st.markdown(":green[Safe / No known irritants] 🎉")

        with col4:
            pos_ratio = products_final[products_final['product_id'] == p_id]['Pos ratio'].values[0]
            neg_ratio = 1 - pos_ratio
            if pos_ratio == 0.0:
                st.markdown(":blue[No reviews yet!]")
            else:
                st.markdown(f":green[Positive Reviews Percentage {pos_ratio.round(2)*100}%]")
                st.markdown(f":red[Negative Reviews Percentage {neg_ratio.round(2)*100}%]")

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


    /* 8. الخطوط الفاصلة (Divider) */
    hr {
        border-color: #E6D2C8 !important;
    }
    </style>

""", unsafe_allow_html=True)