import streamlit as st
import os
from main import extract_text_from_image, extract_menu_items, generate_recommendations
from PIL import Image
import base64
import matplotlib.pyplot as plt

# App Config
st.set_page_config(page_title="NutriVision AI", layout="wide", page_icon="🥗")
st.title("🥗 NutriVision AI — Your Personal Nutritionist")
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .css-1d391kg, .css-1v0mbdj, .css-18e3th9 {
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar theme toggle
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""<style>body { background-color: #121212; color: white; }</style>""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🔍 Upload Menu (Optional)")
    uploaded_file = st.file_uploader("Upload a menu image (optional)", type=["png", "jpg", "jpeg"])
    menu_items = []
    if uploaded_file:
        image_path = os.path.join("uploads", uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(Image.open(image_path), caption="Uploaded Menu", use_column_width=True)
        extracted_text = extract_text_from_image(image_path)
        menu_items = extract_menu_items(extracted_text)
        if menu_items:
            st.success(f"Extracted items: {', '.join(menu_items[:5])} ...")
        else:
            st.warning("No valid food items detected.")

with col2:
    st.header("🧠 Tell Us About You")
    age = st.slider("Age", 10, 100, 25)
    gender = st.radio("Gender", ["Male", "Female"])
    weight = st.slider("Weight (kg)", 30, 150, 60)
    height = st.slider("Height (cm)", 100, 220, 165)
    diet_type = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
    region = st.selectbox("Cuisine Region", ["Any", "North Indian", "South Indian", "Chinese", "Continental"])
    disease = st.multiselect("Diseases (Optional)", ["Diabetes", "Hypertension", "None"])
    meal_time = st.selectbox("Meal Type", ["Any", "Breakfast", "Lunch", "Dinner"])
    goal = st.radio("Fitness Goal", ["Maintain Weight", "Fat Loss", "Muscle Gain"])

if st.button("🍽️ Get Diet Recommendations"):
    selected_disease = " ".join(d for d in disease if d != "None") if disease else ""
    result = generate_recommendations(age, gender, weight, height, diet_type, selected_disease, region, meal_time, menu_items, goal)

    st.subheader("📊 Your Daily Nutritional Breakdown")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("Calories (kcal)", result['calories'])
        st.metric("Protein (g)", result['protein'])
        st.metric("Fat (g)", result['fat'])
        st.metric("Carbs (g)", result['carbs'])

    with col2:
        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        labels = ['Protein', 'Fat', 'Carbs']
        sizes = [result['protein'], result['fat'], result['carbs']]
        colors = ['#4CAF50', '#FF9800', '#03A9F4']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        st.pyplot(fig)

    st.subheader("🥗 Recommended Foods")
    for food in result['foods']:
        st.success(f"✅ {food['name']} ({food['region']} | {food['meal']} | {food['diet']})")

    st.markdown("---")
    st.markdown("**Note:** These recommendations are based on your inputs and standard nutritional models.")
