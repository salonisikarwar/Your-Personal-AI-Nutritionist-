import re
import numpy as np
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_text_from_image(image_path):
    import easyocr
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_path, detail=0)
    return " ".join(result)

def extract_menu_items(text):
    lines = re.split(r'\n|,|;', text)
    menu_items = [line.strip().lower() for line in lines if 2 < len(line.strip()) <= 40]
    return list(set(menu_items))

def classify_text(text, labels):
    result = classifier(text, labels)
    return result["labels"][0] if result["scores"][0] > 0.5 else "Other"

def calculate_bmr(age, gender, weight, height):
    # Mifflin-St Jeor Equation
    if gender.lower() == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def get_macro_split(goal):
    # Macronutrient % splits by goal
    if goal == "Muscle Gain":
        return {"protein": 0.35, "fat": 0.25, "carbs": 0.4}
    elif goal == "Fat Loss":
        return {"protein": 0.4, "fat": 0.3, "carbs": 0.3}
    else:
        return {"protein": 0.3, "fat": 0.25, "carbs": 0.45}

def generate_recommendations(age, gender, weight, height, diet_type, disease, region, meal_time, menu_items, goal):
    # Calculate BMR and macros
    bmr = calculate_bmr(age, gender, weight, height)
    if goal == "Fat Loss":
        calories = bmr - 300
    elif goal == "Muscle Gain":
        calories = bmr + 300
    else:
        calories = bmr

    macros_split = get_macro_split(goal)
    protein_g = round((macros_split["protein"] * calories) / 4)
    fat_g = round((macros_split["fat"] * calories) / 9)
    carbs_g = round((macros_split["carbs"] * calories) / 4)

    # Food knowledge base (can be expanded)
    food_db = [
        {"name": "Grilled Chicken", "region": "North Indian", "diet": "Non-Vegetarian", "meal": "Lunch", "tags": ["muscle", "protein"]},
        {"name": "Paneer Tikka", "region": "North Indian", "diet": "Vegetarian", "meal": "Dinner", "tags": ["protein", "muscle"]},
        {"name": "Mixed Veg Khichdi", "region": "South Indian", "diet": "Vegetarian", "meal": "Dinner", "tags": ["fiber", "light"]},
        {"name": "Quinoa Salad", "region": "Continental", "diet": "Vegetarian", "meal": "Lunch", "tags": ["fat loss", "fiber"]},
        {"name": "Boiled Eggs", "region": "Any", "diet": "Non-Vegetarian", "meal": "Breakfast", "tags": ["protein"]},
        {"name": "Oats with Milk", "region": "Any", "diet": "Vegetarian", "meal": "Breakfast", "tags": ["carbs", "fiber"]},
        {"name": "Grilled Fish", "region": "Any", "diet": "Non-Vegetarian", "meal": "Dinner", "tags": ["omega", "muscle"]},
        {"name": "Tofu Stir Fry", "region": "Chinese", "diet": "Vegetarian", "meal": "Lunch", "tags": ["muscle", "vegan"]},
    ]

    # Filter logic
    filtered = []
    for food in food_db:
        if food["diet"] != diet_type:
            continue
        if region and food["region"] != "Any" and region != food["region"]:
            continue
        if meal_time != "Any" and food["meal"] != meal_time:
            continue
        if disease and disease.lower() in food["tags"]:
            continue
        if goal.lower() not in " ".join(food["tags"]):
            continue
        filtered.append(food)

    # If menu items uploaded, check for matches
    if menu_items:
        menu_filtered = [f for f in filtered if any(item in f["name"].lower() for item in menu_items)]
        if menu_filtered:
            filtered = menu_filtered

    if not filtered:
        filtered = food_db[:3]  # Minimal fallback from original DB (better than generic random)

    return {
        "calories": int(calories),
        "protein": protein_g,
        "fat": fat_g,
        "carbs": carbs_g,
        "foods": filtered
    }
