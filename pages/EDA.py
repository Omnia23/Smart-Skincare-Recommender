import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import os
import gdown

# Reading Data
@st.cache_data
def load_data():
    products = pd.read_csv('products_cleaned.csv')
    file_id = '1xwxNRoYygTJ525FbgRU8oUB5ofqQptsG'
    output = 'reviews_cleaned.csv'
    if not os.path.exists(output):
        gdown.download(id=file_id, output=output, quiet=False)
    reviews = pd.read_csv(output)
    return products, reviews
products , reviews = load_data()
# Streamlit
st.set_page_config(
    page_title='Exploratory Data Analysis',
    page_icon='📉',
    layout='wide',
    initial_sidebar_state='expanded'
)
st.title('Unveiling the Story Behind Skincare Data🧴✨')
st.write(''' **Exploratory Data Analysis (EDA)** in AI is the critical first phase where 
data scientists inspect, clean, and summarize data using stats 
and graphs before training machine learning models ''')
# --------------------------- 1️⃣ EDA for Products Table ------------------------
st.dataframe(
    products.head(10),
    use_container_width=True,
    hide_index=True
)

# الواحد ربك هو الواحد ويلا اول شارت
temp = (
    products.groupby('product_name')[['rating', 'loves_count']]
    .mean()
    .reset_index()
    .sort_values(by='loves_count', ascending=False)
)
temp['rating_int'] = temp['rating'].round()
x = temp['rating_int'].value_counts().sort_index()
fig_pie = px.pie(
    names=x.index,
    values=x.values,
    title='Rating Distribution',
    color_discrete_sequence=px.colors.qualitative.Pastel1,
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_pie.update_layout(title_x=0.5)

top5_products = temp.head(5).copy()
top5_products['short_name'] = top5_products['product_name'].apply(
    lambda x: x[:25] + '...' if len(x) > 25 else x
)

fig_bar = px.bar(
    top5_products,
    y='short_name',
    x='loves_count',
    title='Top 5 products by loves count',
    color='loves_count',
    color_continuous_scale='Magenta',
    labels={'short_name': 'Product Name', 'loves_count': 'Loves Count'},
)
fig_bar.update_layout(title_x=0.5)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.plotly_chart(fig_bar, use_container_width=True)

# اتنين يالحسن والحسين
fig = px.box(
    products,
    y='price_usd',
    x='primary_category',
    hover_data=['product_name'],
    color_discrete_sequence=px.colors.qualitative.Pastel1,
)
fig.update_layout(
    title={
        'text': "Price Distribution",
        'x': 0.5,
        'xanchor': 'center',
    },
    xaxis_title='Primary Category',
    yaxis_title='Price (USD)',
)
st.plotly_chart(fig, use_container_width=True)
# تلاتة بالله العظيم ما جاي هنا تاني
temp = (
    pd.pivot_table(
        data=products[products['primary_category'] == 'Skincare'],
        index='secondary_category',
        values=['product_id', 'price_usd', 'rating'],
        aggfunc={
            'product_id': 'count',
            'price_usd': 'mean',
            'rating': 'mean',
        },
    )
    .reset_index()
    .rename(
        columns={
            'product_id': 'count',
            'price_usd': 'avg price',
            'rating': 'avg rate',
        }
    )
    .round(2)
)
st.markdown("### 🧴 Skincare Categories Breakdown")
st.dataframe(
    temp,
    use_container_width=True,
    hide_index=True,
)
st.markdown("")
st.divider()
# --------------------------- 2️⃣ EDA for Reviews Table ------------------------
st.title("Over than 1M review based on Customers Experience")
st.dataframe(
    reviews.head(10),
    use_container_width=True,
    hide_index=True,
)

# اربعة صحبتنا حلوة مربعة

fig_rating = px.histogram(
    reviews,
    x='rating',
    color='is_recommended',
    barmode='group',
    title='Rating Distribution VS Is Recommended',
    color_discrete_sequence=['#F5AFAF', '#FFF3C8'],
    labels={
        'rating': 'Rating',
        'is_recommended': 'Is Recommended',
        'count': 'Count',
    },
)
fig_rating.update_layout(
    title_x=0.5,
    yaxis_title='Count',
    legend_title_text='Recommended',
)
st.plotly_chart(fig_rating, use_container_width=True)

# الخمسة عدد صوابع الايد
temp = reviews.groupby('brand_name')[['rating',
                                      'total_pos_feedback_count',
                                      'total_neg_feedback_count']].mean().round(2).reset_index().sort_values(by='rating' , ascending=False)
fig = px.bar(
    temp.head(10),
    x='brand_name',
    y='rating',
    color='rating',
    color_continuous_scale='RdPu',
)

fig.update_layout(
    title_text='Top 10 Brands Rating',
    title_x=0.5,
    xaxis_title='Brand Name',
    yaxis_title='Rating',
    yaxis=dict(range=[0, 5]),
)
st.plotly_chart(fig, use_container_width=True)
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
    
    th {
        background-color: #FEEBF6 !important;
        color: #D81B60 !important; 
        font-weight: bold !important;
        text-align: center !important;
    }
   td {
        background-color: #FFF5F9 !important; 
        color: #4A4A4A !important;           
        border: 1px solid #FEEBF6 !important; 
    }
    /* 8. الخطوط الفاصلة (Divider) */
    hr {
        border-color: #E6D2C8 !important;
    }
    </style>

""", unsafe_allow_html=True)




