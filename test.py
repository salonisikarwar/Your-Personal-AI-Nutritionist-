from main import (
    extract_text_from_image,
    extract_menu_items,
    generate_recommendations
)

# Sample test data
test_image_path = "uploads/sample_menu.jpg"  # Make sure this image exists
age = 25
gender = "female"
weight = 60  # in kg
height = 165  # in cm
diet_type = "Vegetarian"
disease = "diabetes"
region = "North Indian"
meal_time = "Lunch"
goal = "Fat Loss"

# ---- Step 1: Extract text from image ----
try:
    extracted_text = extract_text_from_image(test_image_path)
    print("Extracted Text:\n", extracted_text)
except Exception as e:
    print("OCR Extraction Failed:", e)
    extracted_text = ""

# ---- Step 2: Extract menu items ----
menu_items = extract_menu_items(extracted_text)
print("\nMenu Items Found:", menu_items)

# ---- Step 3: Generate recommendations ----
result = generate_recommendations(
    age=age,
    gender=gender,
    weight=weight,
    height=height,
    diet_type=diet_type,
    disease=disease,
    region=region,
    meal_time=meal_time,
    menu_items=menu_items,
    goal=goal
)

# ---- Step 4: Display results ----
print("\n--- Personalized Diet Plan ---")
print(f"Total Calories: {result['calories']} kcal")
print(f"Protein: {result['protein']} g")
print(f"Fat: {result['fat']} g")
print(f"Carbs: {result['carbs']} g")
print("\nRecommended Foods:")
for food in result["foods"]:
    print(f"- {food['name']} ({food['meal']}, {food['region']}, {food['diet']})")

