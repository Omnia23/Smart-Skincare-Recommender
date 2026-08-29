import warnings
import nltk
import numpy as np
import pandas as pd
import streamlit as st

nltk.download('stopwords')
warnings.filterwarnings('ignore')

products = pd.read_csv('products_cleaned.csv')
prod_ings = pd.read_csv('prod_ing_cleaned.csv')
prod_high = pd.read_csv('prod_high_cleaned.csv')

skin_care = products[products['primary_category'] == 'Skincare']

skincare_ing = pd.merge(
    skin_care[['product_id', 'product_name', 'rating']],
    prod_ings,
    how='left',
    on='product_id',
)

skincare_ing['ingredients'] = skincare_ing['ingredients'].fillna(
    skincare_ing['product_name']
)

# Lowercase
skincare_ing['ingredients'] = skincare_ing['ingredients'].str.lower()
skincare_ing['ingredients'] = skincare_ing['ingredients'].str.replace(
    r'[^\w\s]', ' ', regex=True
)
skincare_ing['ingredients'] = (
    skincare_ing['ingredients']
    .str.replace(r'\b\d+\.?\d*\b\s*%?', '', regex=True)
    .str.strip()
)

primary_actives = {
    'blackhead': ['salicylic acid','bha','charcoal','clay','kaolin','glycolic acid'],
    'comedonical-acne': ['salicylic acid','bha','niacinamide','azelaic acid','retinol','adapalene'],
    'pustule-acne': ['benzoyl peroxide','salicylic acid','tea tree','sulfur','zinc pca',],
    'eczema': ['ceramide','colloidal oatmeal','allantoin','panthenol','squalane','shea butter',],
    'rosacea': ['azelaic acid','centella','cica','niacinamide','aloe','panthenol','green tea'],
    'wrinkle': ['retinol','retinoid','peptide','adenosine','bakuchiol','collagen','vitamin c'],
}

supportive_rules = {
    'glycerin','water','aqua','hyaluronic','butylene glycol','titanium dioxide','zinc oxide','ethylhexyl methoxycinnamate',
    'extract','oil','algae','rice bran','berry','wax','triglyceride','stearate','cera','butter',}

irritant_ingredients = [
    'fragrance','parfum','alcohol denat','essential oil',
    'limonene','linalool']

product_ingredients_text = (
    skincare_ing.groupby('product_id')['ingredients']
    .apply(lambda x: ' '.join(x))
    .to_dict()
)

prducts_names = (
    skincare_ing.groupby('product_id')['product_name'].first().to_dict()
)
uni_products = skincare_ing['product_id'].unique()

def get_recommendations(user_problems, top_n=5):
    products_score = {}

    for problem in user_problems:
        actvs = primary_actives.get(problem, [])
        for product in uni_products:
            ing_text = product_ingredients_text.get(product, '')
            flag = sum(1 for actv in actvs if actv in ing_text)
            if flag > 0:
                products_score[product] = products_score.get(product, 0) + flag

    top_products = sorted(
        products_score.items(), key=lambda x: x[1], reverse=True)[: top_n]
    return top_products


def get_profile(user_problems):
    reco_products = get_recommendations(user_problems)
    profile = {}
    for product in reco_products:
        product_id = product[0]
        product_name = prducts_names[product_id]
        ing_text = product_ingredients_text.get(product_id, '')
        primary_ings = list({
            ing
            for problem in user_problems
            for ing in primary_actives.get(problem, [])
            if ing in ing_text
        })

        supportive_ings = [
            ing for ing in supportive_rules if ing in ing_text
        ]
        irr_ings = [ing for ing in irritant_ingredients if ing in ing_text]

        profile[product_id] = {
            'product_name': product_name,
            'primary_ings': primary_ings,
            'supportive_ings': supportive_ings,
            'irr_ings': irr_ings,
        }
    return profile