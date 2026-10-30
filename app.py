import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="TargetHealth Mobile Tracker",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Multi-User Accounts
USERS = {
    "Rogee": "user1pass",
    "Rey": "user2pass",
    "User 3 (John)": "user3pass",
    "User 4 (Sarah)": "user4pass"
}

# 70+ Extended Food Items
FOOD_DATA = [
    # VEGETABLES & GREENS
    {"Category": "Vegetables & Greens", "Food Item": "Spinach (Raw)", "Portion Weight (g)": 100, "Portion Type": "Cupped Hand / 1 Cup", "Calories (kcal)": 23, "Carbs/Sugar (g)": 3.6, "GI": 15, "Sodium (mg)": 79, "Potassium (mg)": 558, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit A, C, K, Iron, Folate", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Broccoli (Steamed)", "Portion Weight (g)": 100, "Portion Type": "Fist Size / 1 Cup", "Calories (kcal)": 35, "Carbs/Sugar (g)": 7.2, "GI": 15, "Sodium (mg)": 33, "Potassium (mg)": 316, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Vit C, K, Fiber, Sulforaphane", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Cucumber (With Peel)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Cucumber", "Calories (kcal)": 15, "Carbs/Sugar (g)": 3.6, "GI": 15, "Sodium (mg)": 2, "Potassium (mg)": 147, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit K, Water, Potassium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Cauliflower (Boiled)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Chopped", "Calories (kcal)": 23, "Carbs/Sugar (g)": 4.1, "GI": 15, "Sodium (mg)": 15, "Potassium (mg)": 142, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Vit C, K, Choline", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Kale (Raw)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Chopped", "Calories (kcal)": 49, "Carbs/Sugar (g)": 8.8, "GI": 15, "Sodium (mg)": 38, "Potassium (mg)": 447, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit A, C, K, Calcium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Carrots (Raw Sliced)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Carrot", "Calories (kcal)": 41, "Carbs/Sugar (g)": 9.6, "GI": 39, "Sodium (mg)": 69, "Potassium (mg)": 320, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Beta-Carotene, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Tomatoes (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Tomato", "Calories (kcal)": 18, "Carbs/Sugar (g)": 3.9, "GI": 15, "Sodium (mg)": 5, "Potassium (mg)": 237, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Lycopene, Vit C, Potassium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Bell Pepper (Red/Green)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Pepper", "Calories (kcal)": 26, "Carbs/Sugar (g)": 6.0, "GI": 15, "Sodium (mg)": 3, "Potassium (mg)": 211, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C, Vit B6, Antioxidants", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Asparagus (Cooked)", "Portion Weight (g)": 100, "Portion Type": "5-6 Spears", "Calories (kcal)": 22, "Carbs/Sugar (g)": 3.9, "GI": 15, "Sodium (mg)": 14, "Potassium (mg)": 224, "Sat Fat (g)": 0.0, "Purine Level": "Moderate", "Vitamins & Nutrients": "Folate, Vit K, Glutathione", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Celery (Raw)", "Portion Weight (g)": 100, "Portion Type": "2 Stalks", "Calories (kcal)": 14, "Carbs/Sugar (g)": 3.0, "GI": 15, "Sodium (mg)": 80, "Potassium (mg)": 260, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Phthalides, Vit K, Water", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Garlic (Fresh)", "Portion Weight (g)": 10, "Portion Type": "2-3 Cloves", "Calories (kcal)": 15, "Carbs/Sugar (g)": 3.3, "GI": 15, "Sodium (mg)": 2, "Potassium (mg)": 40, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Allicin, S-Allylcysteine", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Sweet Potato (Baked)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Potato", "Calories (kcal)": 90, "Carbs/Sugar (g)": 20.7, "GI": 54, "Sodium (mg)": 36, "Potassium (mg)": 475, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit A, Fiber, Potassium", "HbA1c Status": "Acceptable", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # FRUITS & BERRIES
    {"Category": "Fruits & Berries", "Food Item": "Tart Cherries (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1 Handful / 10-12 Cherries", "Calories (kcal)": 50, "Carbs/Sugar (g)": 12.2, "GI": 22, "Sodium (mg)": 0, "Potassium (mg)": 173, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Anthocyanins, Vit C", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Blueberries (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1 Cupped Handful", "Calories (kcal)": 57, "Carbs/Sugar (g)": 14.5, "GI": 53, "Sodium (mg)": 1, "Potassium (mg)": 77, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C, K, Manganese, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Strawberries (Fresh)", "Portion Weight (g)": 100, "Portion Type": "5-6 Medium Strawberries", "Calories (kcal)": 32, "Carbs/Sugar (g)": 7.7, "GI": 41, "Sodium (mg)": 1, "Potassium (mg)": 153, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C, Folate, Polyphenols", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Green Apple (With Skin)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Apple", "Calories (kcal)": 52, "Carbs/Sugar (g)": 13.8, "GI": 36, "Sodium (mg)": 1, "Potassium (mg)": 107, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Pectin Fiber, Vit C", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Avocado (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1/2 Medium Avocado", "Calories (kcal)": 160, "Carbs/Sugar (g)": 8.5, "GI": 15, "Sodium (mg)": 7, "Potassium (mg)": 485, "Sat Fat (g)": 2.1, "Purine Level": "Low", "Vitamins & Nutrients": "Monounsaturated Fat, Potassium, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Orange (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Orange", "Calories (kcal)": 47, "Carbs/Sugar (g)": 11.8, "GI": 43, "Sodium (mg)": 0, "Potassium (mg)": 181, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C, Hesperidin, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Grapefruit (Pink)", "Portion Weight (g)": 100, "Portion Type": "1/2 Medium Grapefruit", "Calories (kcal)": 42, "Carbs/Sugar (g)": 10.7, "GI": 25, "Sodium (mg)": 0, "Potassium (mg)": 135, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Naringenin, Vit C, Vit A", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Banana (Medium)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Banana", "Calories (kcal)": 89, "Carbs/Sugar (g)": 22.8, "GI": 51, "Sodium (mg)": 1, "Potassium (mg)": 358, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Potassium, Vit B6, Resistant Starch", "HbA1c Status": "Acceptable", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Fruits & Berries", "Food Item": "Watermelon", "Portion Weight (g)": 100, "Portion Type": "1 Wedge / 1 Cup Wedges", "Calories (kcal)": 30, "Carbs/Sugar (g)": 7.5, "GI": 72, "Sodium (mg)": 1, "Potassium (mg)": 112, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Lycopene, Vit A, C", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Not Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Papaya (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Cubes", "Calories (kcal)": 43, "Carbs/Sugar (g)": 10.8, "GI": 60, "Sodium (mg)": 8, "Potassium (mg)": 182, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Papain Enzyme, Vit C, Folate", "HbA1c Status": "Acceptable", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Fruits & Berries", "Food Item": "Lemon / Lime Juice", "Portion Weight (g)": 30, "Portion Type": "2 tbsp / Juice of 1 Lemon", "Calories (kcal)": 8, "Carbs/Sugar (g)": 2.5, "GI": 20, "Sodium (mg)": 1, "Potassium (mg)": 35, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Citrate (Prevents Urate Stones), Vit C", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # GRAINS & LEGUMES
    {"Category": "Grains & Legumes", "Food Item": "Rolled Oats (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Cooked / Fist Size", "Calories (kcal)": 71, "Carbs/Sugar (g)": 12.0, "GI": 55, "Sodium (mg)": 1, "Potassium (mg)": 61, "Sat Fat (g)": 0.3, "Purine Level": "Low", "Vitamins & Nutrients": "Beta-Glucan Fiber, B-Vitamins", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Lentils (Boiled)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 116, "Carbs/Sugar (g)": 20.1, "GI": 32, "Sodium (mg)": 2, "Potassium (mg)": 369, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Folate, Fiber, Plant Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Grains & Legumes", "Food Item": "Quinoa (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 120, "Carbs/Sugar (g)": 21.3, "GI": 53, "Sodium (mg)": 7, "Potassium (mg)": 172, "Sat Fat (g)": 0.2, "Purine Level": "Low", "Vitamins & Nutrients": "Magnesium, Iron, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Chickpeas (Boiled)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 164, "Carbs/Sugar (g)": 27.4, "GI": 28, "Sodium (mg)": 7, "Potassium (mg)": 291, "Sat Fat (g)": 0.3, "Purine Level": "Moderate", "Vitamins & Nutrients": "Protein, Soluble Fiber, Folate", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Grains & Legumes", "Food Item": "Brown Rice (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 123, "Carbs/Sugar (g)": 25.6, "GI": 68, "Sodium (mg)": 1, "Potassium (mg)": 86, "Sat Fat (g)": 0.2, "Purine Level": "Low", "Vitamins & Nutrients": "Magnesium, B6, Fiber", "HbA1c Status": "Acceptable", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Grains & Legumes", "Food Item": "White Rice (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 130, "Carbs/Sugar (g)": 28.2, "GI": 73, "Sodium (mg)": 1, "Potassium (mg)": 35, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Refined Starch", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Not Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Whole Wheat Bread", "Portion Weight (g)": 35, "Portion Type": "1 Medium Slice", "Calories (kcal)": 81, "Carbs/Sugar (g)": 13.8, "GI": 51, "Sodium (mg)": 132, "Potassium (mg)": 81, "Sat Fat (g)": 0.2, "Purine Level": "Low", "Vitamins & Nutrients": "Whole Grain Fiber, Selenium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Acceptable", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "White Bread", "Portion Weight (g)": 35, "Portion Type": "1 Medium Slice", "Calories (kcal)": 93, "Carbs/Sugar (g)": 17.2, "GI": 75, "Sodium (mg)": 170, "Potassium (mg)": 40, "Sat Fat (g)": 0.2, "Purine Level": "Low", "Vitamins & Nutrients": "Refined Starch, Added Salt", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Acceptable", "Hypertension Status": "Not Allowed", "Overall Suitability": "Not Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Buckwheat (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 92, "Carbs/Sugar (g)": 19.9, "GI": 45, "Sodium (mg)": 1, "Potassium (mg)": 88, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Rutin (Lowers BP), Magnesium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # PROTEINS & SEAFOOD
    {"Category": "Proteins & Seafood", "Food Item": "Chicken Breast (Skinless)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 140, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 63, "Potassium (mg)": 218, "Sat Fat (g)": 0.9, "Purine Level": "Moderate", "Vitamins & Nutrients": "Niacin, Vit B6, Lean Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Turkey Breast (Skinless)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 125, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 55, "Potassium (mg)": 250, "Sat Fat (g)": 0.6, "Purine Level": "Moderate", "Vitamins & Nutrients": "Tryptophan, Selenium, B-Vitamins", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Salmon Fillet (Grilled)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 175, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 50, "Potassium (mg)": 309, "Sat Fat (g)": 1.3, "Purine Level": "Moderate", "Vitamins & Nutrients": "Omega-3 EPA/DHA, Vit D", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Cod / White Fish (Baked)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 90, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 65, "Potassium (mg)": 350, "Sat Fat (g)": 0.2, "Purine Level": "Moderate", "Vitamins & Nutrients": "Very Lean Protein, Iodine", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Tofu (Firm)", "Portion Weight (g)": 100, "Portion Type": "Palm Size Block", "Calories (kcal)": 83, "Carbs/Sugar (g)": 1.9, "GI": 15, "Sodium (mg)": 12, "Potassium (mg)": 121, "Sat Fat (g)": 0.8, "Purine Level": "Low", "Vitamins & Nutrients": "Isoflavones, Calcium, Plant Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Proteins & Seafood", "Food Item": "Organ Meats (Beef Liver)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 149, "Carbs/Sugar (g)": 4.4, "GI": 0, "Sodium (mg)": 59, "Potassium (mg)": 280, "Sat Fat (g)": 1.5, "Purine Level": "Very High", "Vitamins & Nutrients": "Vit A, B12, Iron (HIGH PURINE)", "HbA1c Status": "Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Not Allowed", "Hypertension Status": "Acceptable", "Overall Suitability": "Not Allowed"},
    {"Category": "Proteins & Seafood", "Food Item": "Sardines (In Water)", "Portion Weight (g)": 85, "Portion Type": "1 Small Can", "Calories (kcal)": 177, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 260, "Potassium (mg)": 337, "Sat Fat (g)": 1.3, "Purine Level": "High", "Vitamins & Nutrients": "Calcium, Vit D, Omega-3", "HbA1c Status": "Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Acceptable", "Overall Suitability": "Not Allowed"},
    {"Category": "Proteins & Seafood", "Food Item": "Shrimp (Steamed)", "Portion Weight (g)": 85, "Portion Type": "5-6 Medium Shrimp", "Calories (kcal)": 84, "Carbs/Sugar (g)": 0.2, "GI": 0, "Sodium (mg)": 190, "Potassium (mg)": 185, "Sat Fat (g)": 0.2, "Purine Level": "High", "Vitamins & Nutrients": "Astaxanthin, Selenium", "HbA1c Status": "Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Acceptable", "Hypertension Status": "Acceptable", "Overall Suitability": "Not Allowed"},

    # EGGS & DAIRY
    {"Category": "Eggs & Dairy", "Food Item": "Egg White (Boiled)", "Portion Weight (g)": 33, "Portion Type": "1 Large Egg White", "Calories (kcal)": 17, "Carbs/Sugar (g)": 0.2, "GI": 0, "Sodium (mg)": 55, "Potassium (mg)": 54, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Pure Ovalbumin Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Whole Egg (Boiled)", "Portion Weight (g)": 50, "Portion Type": "1 Large Egg", "Calories (kcal)": 72, "Carbs/Sugar (g)": 0.4, "GI": 0, "Sodium (mg)": 71, "Potassium (mg)": 69, "Sat Fat (g)": 1.6, "Purine Level": "Zero", "Vitamins & Nutrients": "Choline, Lutein, Vit D", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Acceptable", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Non-Fat Greek Yogurt", "Portion Weight (g)": 170, "Portion Type": "1 Individual Container (6 oz)", "Calories (kcal)": 100, "Carbs/Sugar (g)": 6.1, "GI": 12, "Sodium (mg)": 61, "Potassium (mg)": 240, "Sat Fat (g)": 0.2, "Purine Level": "Zero", "Vitamins & Nutrients": "Probiotics, Calcium, Uric Acid Lowering", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Skim Milk (0%)", "Portion Weight (g)": 245, "Portion Type": "1 Glass / 1 Cup", "Calories (kcal)": 83, "Carbs/Sugar (g)": 12.2, "GI": 32, "Sodium (mg)": 103, "Potassium (mg)": 382, "Sat Fat (g)": 0.1, "Purine Level": "Zero", "Vitamins & Nutrients": "Calcium, Potassium, Vit D", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Whole Milk (3.25%)", "Portion Weight (g)": 245, "Portion Type": "1 Glass / 1 Cup", "Calories (kcal)": 149, "Carbs/Sugar (g)": 11.7, "GI": 39, "Sodium (mg)": 105, "Potassium (mg)": 322, "Sat Fat (g)": 4.6, "Purine Level": "Zero", "Vitamins & Nutrients": "Calcium, Vit D", "HbA1c Status": "Acceptable", "Uric Acid Status": "Allowed", "Cholesterol Status": "Not Allowed", "Hypertension Status": "Acceptable", "Overall Suitability": "Not Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Cheddar Cheese", "Portion Weight (g)": 28, "Portion Type": "1 Slice / 1 Matchbox Slice", "Calories (kcal)": 113, "Carbs/Sugar (g)": 0.4, "GI": 0, "Sodium (mg)": 174, "Potassium (mg)": 27, "Sat Fat (g)": 5.3, "Purine Level": "Zero", "Vitamins & Nutrients": "Calcium, Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Not Allowed", "Hypertension Status": "Not Allowed", "Overall Suitability": "Not Allowed"},

    # NUTS & SEEDS
    {"Category": "Nuts & Seeds", "Food Item": "Walnuts (Raw)", "Portion Weight (g)": 30, "Portion Type": "1 Small Handful (approx 7 halves)", "Calories (kcal)": 196, "Carbs/Sugar (g)": 4.1, "GI": 15, "Sodium (mg)": 1, "Potassium (mg)": 132, "Sat Fat (g)": 1.8, "Purine Level": "Low", "Vitamins & Nutrients": "ALA Omega-3, Magnesium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Nuts & Seeds", "Food Item": "Almonds (Unsalted Raw)", "Portion Weight (g)": 30, "Portion Type": "1 Small Handful (approx 23 nuts)", "Calories (kcal)": 173, "Carbs/Sugar (g)": 6.1, "GI": 15, "Sodium (mg)": 0, "Potassium (mg)": 211, "Sat Fat (g)": 1.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit E, Magnesium, Arginine (Lowers BP)", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Nuts & Seeds", "Food Item": "Chia Seeds (Dry)", "Portion Weight (g)": 15, "Portion Type": "1 Tablespoon", "Calories (kcal)": 73, "Carbs/Sugar (g)": 6.3, "GI": 1, "Sodium (mg)": 2, "Potassium (mg)": 61, "Sat Fat (g)": 0.5, "Purine Level": "Low", "Vitamins & Nutrients": "Soluble Fiber, Calcium, ALA", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Nuts & Seeds", "Food Item": "Flaxseeds (Ground)", "Portion Weight (g)": 15, "Portion Type": "1 Tablespoon", "Calories (kcal)": 55, "Carbs/Sugar (g)": 3.0, "GI": 35, "Sodium (mg)": 3, "Potassium (mg)": 84, "Sat Fat (g)": 0.4, "Purine Level": "Low", "Vitamins & Nutrients": "Lignans, ALA Omega-3, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Nuts & Seeds", "Food Item": "Natural Peanut Butter", "Portion Weight (g)": 32, "Portion Type": "2 Tablespoons", "Calories (kcal)": 188, "Carbs/Sugar (g)": 6.3, "GI": 14, "Sodium (mg)": 5, "Potassium (mg)": 189, "Sat Fat (g)": 3.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit E, Niacin, Healthy Fats", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # BEVERAGES & SWEETS
    {"Category": "Beverages & Sweets", "Food Item": "Green Tea (Unsweetened)", "Portion Weight (g)": 240, "Portion Type": "1 Mug / Cup", "Calories (kcal)": 2, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 2, "Potassium (mg)": 20, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "EGCG Catechins, Antioxidants", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Beverages & Sweets", "Food Item": "Black Coffee (Unsweetened)", "Portion Weight (g)": 240, "Portion Type": "1 Mug / Cup", "Calories (kcal)": 2, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 5, "Potassium (mg)": 116, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Chlorogenic Acid (Lowers Uric Acid)", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Beverages & Sweets", "Food Item": "Regular Soda (Sweetened)", "Portion Weight (g)": 355, "Portion Type": "1 Standard Can (12 oz)", "Calories (kcal)": 135, "Carbs/Sugar (g)": 37.6, "GI": 63, "Sodium (mg)": 14, "Potassium (mg)": 7, "Sat Fat (g)": 0.0, "Purine Level": "High (HFCS)", "Vitamins & Nutrients": "High Fructose Corn Syrup", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Not Allowed", "Hypertension Status": "Not Allowed", "Overall Suitability": "Not Allowed"},
    {"Category": "Beverages & Sweets", "Food Item": "Dark Chocolate 85%", "Portion Weight (g)": 20, "Portion Type": "2 Small Squares", "Calories (kcal)": 120, "Carbs/Sugar (g)": 7.2, "GI": 23, "Sodium (mg)": 4, "Potassium (mg)": 143, "Sat Fat (g)": 5.0, "Purine Level": "Low", "Vitamins & Nutrients": "Flavanols (Lowers BP), Magnesium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Acceptable", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Beverages & Sweets", "Food Item": "Extra Virgin Olive Oil", "Portion Weight (g)": 14, "Portion Type": "1 Tablespoon", "Calories (kcal)": 119, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 0, "Potassium (mg)": 0, "Sat Fat (g)": 1.9, "Purine Level": "Zero", "Vitamins & Nutrients": "Oleic Acid, Polyphenols (AHA Approved)", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"}
]

def load_database():
    df = pd.DataFrame(FOOD_DATA)
    # Guarantee key columns exist even if old cached data is loaded
    if "Portion Type" not in df.columns:
        df["Portion Type"] = "Standard Portion"
    if "Hypertension Status" not in df.columns:
        df["Hypertension Status"] = "Allowed"
    return df

df_db = load_database()

# Session States
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if "user_logs" not in st.session_state:
    st.session_state.user_logs = {u: [] for u in USERS.keys()}

if "user_exercise" not in st.session_state:
    st.session_state.user_exercise = {u: [] for u in USERS.keys()}

if "user_bp" not in st.session_state:
    st.session_state.user_bp = {u: [] for u in USERS.keys()}

# Login View
if st.session_state.authenticated_user is None:
    st.title("🔐 TargetHealth Mobile Login")
    st.info("Please select your profile and enter your password:")
    
    col_l1, col_l2 = st.columns([1, 1])
    with col_l1:
        selected_user = st.selectbox("Select Profile", list(USERS.keys()))
        password_input = st.text_input("Password", type="password")
        if st.button("🔓 Log In", use_container_width=True):
            if password_input == USERS[selected_user]:
                st.session_state.authenticated_user = selected_user
                st.toast(f"Welcome back, {selected_user}!", icon="🎉")
                st.rerun()
            else:
                st.error("Incorrect password.")
    with col_l2:
        st.markdown("### 🔑 Demo Logins:")
        st.code("User 1 (Alex): user1pass\nUser 2 (Maria): user2pass\nUser 3 (John): user3pass\nUser 4 (Sarah): user4pass")
    st.stop()

# Main Logged-In App
active_user = st.session_state.authenticated_user

st.sidebar.markdown(f"👤 **User:** `{active_user}`")
if st.sidebar.button("🚪 Log Out", use_container_width=True):
    st.session_state.authenticated_user = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("🎯 Target Limits")
target_calories = st.sidebar.number_input("Max Calories (kcal)", value=2000, step=100)
target_sugar = st.sidebar.number_input("Max Sugar/Carbs (g) [HbA1c 5.0]", value=25, step=5)
target_sat_fat = st.sidebar.number_input("Max Sat Fat (g) [Cholesterol]", value=13, step=1)
target_sodium = st.sidebar.number_input("Max Sodium (mg) [Hypertension/DASH]", value=1500, step=100)
target_potassium = st.sidebar.number_input("Min Potassium Target (mg)", value=3500, step=100)

st.title("📱 TargetHealth Mobile Tracker")
st.caption(f"Profile: **{active_user}** | Target Controls: HbA1c 5.0%, Uric Acid 5.0 mg/dL, Low LDL, DASH Hypertension")

tab_log, tab_calc, tab_ex, tab_db, tab_dl = st.tabs([
    "⏱️ Food Intake", 
    "⚖️ Weight Estimator", 
    "🔥 Calories & BP", 
    "🔍 Database", 
    "📥 Download"
])

# Tab 1: Food Intake
with tab_log:
    st.subheader("1. Food Check & Quick Logger")
    c1, c2 = st.columns(2)
    with c1:
        cat_choice = st.selectbox("Category", df_db["Category"].unique())
        sub_df = df_db[df_db["Category"] == cat_choice]
        food_choice = st.selectbox("Food Item", sub_df["Food Item"].unique())
        sel_row = sub_df[sub_df["Food Item"] == food_choice].iloc[0]
        meal_type = st.selectbox("Meal / Time", ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner", "Late Snack"])

    with c2:
        st.markdown("💡 **Portion Input Mode:**")
        p_mode = st.radio("Portion Mode", ["Estimated Size (No Scale)", "Custom Grams"], horizontal=True)
        base_g = float(sel_row["Portion Weight (g)"])
        def_label = sel_row["Portion Type"] if "Portion Type" in sel_row else "Standard Portion"
        
        if p_mode == "Estimated Size (No Scale)":
            p_scale = st.select_slider(
                f"Size ({def_label})",
                options=["0.5x (Small/Half)", "1.0x (Standard)", "1.5x (Large)", "2.0x (Double)"],
                value="1.0x (Standard)"
            )
            m_map = {"0.5x (Small/Half)": 0.5, "1.0x (Standard)": 1.0, "1.5x (Large)": 1.5, "2.0x (Double)": 2.0}
            mult = m_map[p_scale]
            portion_g = round(base_g * mult, 1)
            st.info(f"📏 Weight: **{portion_g} grams**")
        else:
            portion_g = st.number_input("Custom Grams", value=int(base_g), min_value=1, max_value=2000, step=5)
            mult = portion_g / base_g

    item_cals = round(sel_row["Calories (kcal)"] * mult, 1)
    item_sugar = round(sel_row["Carbs/Sugar (g)"] * mult, 1)
    item_sat_fat = round(sel_row["Sat Fat (g)"] * mult, 1)
    item_sodium = round(sel_row["Sodium (mg)"] * mult, 1)
    item_potassium = round(sel_row["Potassium (mg)"] * mult, 1)
    suitability = sel_row["Overall Suitability"]
    hyp_status = sel_row["Hypertension Status"] if "Hypertension Status" in sel_row else "Allowed"
    uric_status = sel_row["Uric Acid Status"] if "Uric Acid Status" in sel_row else "Allowed"
    chol_status = sel_row["Cholesterol Status"] if "Cholesterol Status" in sel_row else "Allowed"

    st.markdown("#### 🛡️ Pre-Eat Warning:")
    w1, w2 = st.columns([3, 1])
    with w1:
        if suitability == "Allowed":
            st.success("🟢 **Safe to Eat** — Fits all 4 clinical target guidelines.")
        elif suitability == "Acceptable":
            st.warning(f"🟡 **Moderate Portion Caution** — Portion control needed. (Hypertension: {hyp_status})")
        else:
            st.error(f"🔴 **AVOID / High Risk** — Fails health targets! (Uric Acid: {uric_status}, Cholesterol: {chol_status})")
            
    with w2:
        if st.button("➕ Log Food Intake", use_container_width=True):
            log_entry = {
                "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                "User": active_user,
                "Meal": meal_type,
                "Food Item": food_choice,
                "Category": cat_choice,
                "Weight (g)": portion_g,
                "Calories": item_cals,
                "Sugar/Carbs (g)": item_sugar,
                "Sat Fat (g)": item_sat_fat,
                "Sodium (mg)": item_sodium,
                "Potassium (mg)": item_potassium,
                "Suitability": suitability
            }
            st.session_state.user_logs[active_user].append(log_entry)
            st.toast(f"Logged {food_choice} ({portion_g}g)!", icon="✅")

    st.markdown("---")
    st.subheader("2. Cumulative Allowance Dashboard")
    
    user_log_list = st.session_state.user_logs[active_user]
    if user_log_list:
        df_user_log = pd.DataFrame(user_log_list)
        tot_cals = round(df_user_log["Calories"].sum(), 1)
        tot_sugar = round(df_user_log["Sugar/Carbs (g)"].sum(), 1)
        tot_sat_fat = round(df_user_log["Sat Fat (g)"].sum(), 1)
        tot_sodium = round(df_user_log["Sodium (mg)"].sum(), 1)
        tot_potassium = round(df_user_log["Potassium (mg)"].sum(), 1)
    else:
        df_user_log = pd.DataFrame()
        tot_cals = tot_sugar = tot_sat_fat = tot_sodium = tot_potassium = 0.0

    user_ex_list = st.session_state.user_exercise[active_user]
    cals_burned = sum(e["Calories Burned"] for e in user_ex_list) if user_ex_list else 0.0
    net_cals = round(tot_cals - cals_burned, 1)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Net Calories", f"{net_cals} kcal", f"Food: {tot_cals} | Burned: {cals_burned}")
    m2.metric("Sugar / Carbs", f"{tot_sugar} g", f"{target_sugar - tot_sugar:.1f} g left")
    m3.metric("Sat Fat", f"{tot_sat_fat} g", f"{target_sat_fat - tot_sat_fat:.1f} g left")
    m4.metric("Sodium (DASH)", f"{tot_sodium} mg", f"{target_sodium - tot_sodium:.1f} mg left")
    m5.metric("Potassium", f"{tot_potassium} mg", f"Goal: {target_potassium} mg")

    st.progress(min(max(net_cals / target_calories, 0.0), 1.0), text=f"Net Calories ({net_cals}/{target_calories} kcal)")
    st.progress(min(tot_sodium / target_sodium, 1.0), text=f"Sodium Limit ({tot_sodium}/{target_sodium} mg)")

    if not df_user_log.empty:
        st.markdown("#### 📋 Today's Logged Items:")
        st.dataframe(df_user_log[["Timestamp", "Meal", "Food Item", "Weight (g)", "Calories", "Sugar/Carbs (g)", "Sodium (mg)", "Suitability"]], use_container_width=True)
        if st.button("🗑️ Clear Intake Log"):
            st.session_state.user_logs[active_user] = []
            st.rerun()

# Tab 2: Weight Estimator
with tab_calc:
    st.subheader("⚖️ Visual Portion & Gram Weight Estimator")
    st.markdown("No scale with you? Use hand visual references to estimate weight in grams:")
    
    e1, e2 = st.columns(2)
    with e1:
        est_type = st.selectbox("Visual Guide", [
            "Fist Size (Cooked Rice, Oats, Pasta, Fruits)",
            "Palm of Hand (Lean Meat, Fish, Chicken - 3 oz)",
            "Cupped Handful (Berries, Beans, Chopped Veggies)",
            "Closed Handful (Raw Nuts, Seeds)",
            "1 Tablespoon (Oil, Butter, Peanut Butter, Seeds)",
            "1 Teaspoon (Oil, Sugar, Honey)",
            "1 Slice (Whole Wheat Bread / Cheese)"
        ])
        est_qty = st.number_input("Quantity", value=1.0, min_value=0.25, max_value=10.0, step=0.25)

    g_map = {
        "Fist Size (Cooked Rice, Oats, Pasta, Fruits)": 150,
        "Palm of Hand (Lean Meat, Fish, Chicken - 3 oz)": 85,
        "Cupped Handful (Berries, Beans, Chopped Veggies)": 80,
        "Closed Handful (Raw Nuts, Seeds)": 30,
        "1 Tablespoon (Oil, Butter, Peanut Butter, Seeds)": 15,
        "1 Teaspoon (Oil, Sugar, Honey)": 5,
        "1 Slice (Whole Wheat Bread / Cheese)": 35
    }
    calc_g = round(g_map[est_type] * est_qty, 1)

    with e2:
        st.success(f"📊 **Calculated Estimated Weight:**\n\n### **{calc_g} grams**")
        st.info("💡 Use this weight in the Food Intake tab.")

# Tab 3: Calories Burned & BP
with tab_ex:
    st.subheader("🔥 Exercise & Blood Pressure Tracker")
    ex1, ex2 = st.columns(2)
    with ex1:
        st.markdown("#### 🏃 Log Activity Burn:")
        activity = st.selectbox("Activity", ["Brisk Walking", "Running / Jogging", "Cycling", "Swimming", "Gym / Weight Training", "Household Work"])
        duration = st.number_input("Duration (minutes)", value=30, min_value=5, max_value=300, step=5)
        burn_map = {"Brisk Walking": 4.5, "Running / Jogging": 10.0, "Cycling": 7.0, "Swimming": 8.0, "Gym / Weight Training": 6.0, "Household Work": 3.5}
        est_burned = round(burn_map[activity] * duration, 1)
        st.markdown(f"Estimated Burn: **{est_burned} kcal**")
        if st.button("➕ Log Calories Burned", use_container_width=True):
            st.session_state.user_exercise[active_user].append({
                "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                "Activity": activity,
                "Duration (min)": duration,
                "Calories Burned": est_burned
            })
            st.toast(f"Logged {activity} ({est_burned} kcal)!", icon="🔥")
            st.rerun()

    with ex2:
        st.markdown("#### 🩺 Log Blood Pressure:")
        sys_bp = st.number_input("Systolic (mmHg)", value=120, min_value=70, max_value=220, step=1)
        dia_bp = st.number_input("Diastolic (mmHg)", value=80, min_value=40, max_value=140, step=1)
        
        if sys_bp < 120 and dia_bp < 80:
            bp_status = "🟢 Normal BP"
        elif sys_bp <= 129 and dia_bp < 80:
            bp_status = "🟡 Elevated BP"
        elif sys_bp <= 139 or dia_bp <= 89:
            bp_status = "🟠 Stage 1 Hypertension"
        else:
            bp_status = "🔴 Stage 2 Hypertension"
            
        st.markdown(f"Status: **{bp_status}**")
        if st.button("➕ Log BP Reading", use_container_width=True):
            st.session_state.user_bp[active_user].append({
                "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                "Systolic": sys_bp,
                "Diastolic": dia_bp,
                "Status": bp_status
            })
            st.toast(f"Logged BP {sys_bp}/{dia_bp} mmHg!", icon="🩺")

# Tab 4: Database
with tab_db:
    st.subheader("🔍 Reference Database (70+ Medical Profiles)")
    st.dataframe(df_db, use_container_width=True)

# Tab 5: Download
with tab_dl:
    st.subheader(f"📥 Download Daily Data ({active_user})")
    if user_log_list:
        df_export = pd.DataFrame(user_log_list)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Food Intake Log (.CSV)",
            data=csv_data,
            file_name=f"{active_user.replace(' ', '_')}_food_intake_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No food intake recorded today to download.")
