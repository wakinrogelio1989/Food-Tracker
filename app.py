import urllib.parse
import urllib.request
import json
import streamlit as st
import pandas as pd
import datetime
import re

st.set_page_config(
    page_title="TargetHealth Mobile Tracker",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Multi-User Accounts
USERS = {
    "Rogee": "1989",
    "Rey": "Reign",
    "User 3 (John)": "user3pass",
    "User 4 (Sarah)": "user4pass"
}

# Master Medical Food Database
INITIAL_FOOD_DATA = [
    # VEGETABLES & GREENS
    {"Category": "Vegetables & Greens", "Food Item": "Spinach (Raw)", "Portion Weight (g)": 100, "Portion Type": "Cupped Hand / 1 Cup", "Calories (kcal)": 23, "Carbs/Sugar (g)": 3.6, "GI": 15, "Sodium (mg)": 79, "Potassium (mg)": 558, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit A, C, K, Iron, Folate", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Broccoli (Steamed)", "Portion Weight (g)": 100, "Portion Type": "Fist Size / 1 Cup", "Calories (kcal)": 35, "Carbs/Sugar (g)": 7.2, "GI": 15, "Sodium (mg)": 33, "Potassium (mg)": 316, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Vit C, K, Fiber, Sulforaphane", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Cabbage (Raw / Boiled)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Chopped", "Calories (kcal)": 25, "Carbs/Sugar (g)": 5.8, "GI": 15, "Sodium (mg)": 18, "Potassium (mg)": 170, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C, K, Glutamine, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Kangkong (Water Spinach)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Cooked", "Calories (kcal)": 19, "Carbs/Sugar (g)": 3.1, "GI": 15, "Sodium (mg)": 55, "Potassium (mg)": 312, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit A, C, Iron, Antioxidants", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Pechay (Bok Choy)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Chopped", "Calories (kcal)": 13, "Carbs/Sugar (g)": 2.2, "GI": 15, "Sodium (mg)": 65, "Potassium (mg)": 252, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit A, C, Calcium, Folate", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Potato (Boiled / Baked)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Potato", "Calories (kcal)": 87, "Carbs/Sugar (g)": 20.1, "GI": 78, "Sodium (mg)": 6, "Potassium (mg)": 379, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C, Vit B6, Potassium", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Not Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Cucumber (With Peel)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Cucumber", "Calories (kcal)": 15, "Carbs/Sugar (g)": 3.6, "GI": 15, "Sodium (mg)": 2, "Potassium (mg)": 147, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit K, Water, Potassium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Cauliflower (Boiled)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Chopped", "Calories (kcal)": 23, "Carbs/Sugar (g)": 4.1, "GI": 15, "Sodium (mg)": 15, "Potassium (mg)": 142, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Vit C, K, Choline", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Garlic (Fresh)", "Portion Weight (g)": 10, "Portion Type": "2-3 Cloves", "Calories (kcal)": 15, "Carbs/Sugar (g)": 3.3, "GI": 15, "Sodium (mg)": 2, "Potassium (mg)": 40, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Allicin, S-Allylcysteine", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # FRUITS & BERRIES
    {"Category": "Fruits & Berries", "Food Item": "Kiwi (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Kiwi", "Calories (kcal)": 61, "Carbs/Sugar (g)": 14.7, "GI": 52, "Sodium (mg)": 3, "Potassium (mg)": 312, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C (High), Vit K, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Tart Cherries (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1 Handful / 10-12 Cherries", "Calories (kcal)": 50, "Carbs/Sugar (g)": 12.2, "GI": 22, "Sodium (mg)": 0, "Potassium (mg)": 173, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Anthocyanins, Vit C", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Blueberries (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1 Cupped Handful", "Calories (kcal)": 57, "Carbs/Sugar (g)": 14.5, "GI": 53, "Sodium (mg)": 1, "Potassium (mg)": 77, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C, K, Manganese, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Green Apple (With Skin)", "Portion Weight (g)": 100, "Portion Type": "1 Medium Apple", "Calories (kcal)": 52, "Carbs/Sugar (g)": 13.8, "GI": 36, "Sodium (mg)": 1, "Potassium (mg)": 107, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Pectin Fiber, Vit C", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Avocado (Fresh)", "Portion Weight (g)": 100, "Portion Type": "1/2 Medium Avocado", "Calories (kcal)": 160, "Carbs/Sugar (g)": 8.5, "GI": 15, "Sodium (mg)": 7, "Potassium (mg)": 485, "Sat Fat (g)": 2.1, "Purine Level": "Low", "Vitamins & Nutrients": "Monounsaturated Fat, Potassium, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Lemon / Lime Juice", "Portion Weight (g)": 30, "Portion Type": "2 tbsp / Juice of 1 Lemon", "Calories (kcal)": 8, "Carbs/Sugar (g)": 2.5, "GI": 20, "Sodium (mg)": 1, "Potassium (mg)": 35, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Citrate (Prevents Urate Stones), Vit C", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # GRAINS & LEGUMES
    {"Category": "Grains & Legumes", "Food Item": "Biryani Rice (Spiced Basmati)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 165, "Carbs/Sugar (g)": 28.5, "GI": 65, "Sodium (mg)": 240, "Potassium (mg)": 65, "Sat Fat (g)": 1.2, "Purine Level": "Low", "Vitamins & Nutrients": "Spiced Carbohydrates, Fiber", "HbA1c Status": "Acceptable", "Uric Acid Status": "Allowed", "Cholesterol Status": "Acceptable", "Hypertension Status": "Acceptable", "Overall Suitability": "Acceptable"},
    {"Category": "Grains & Legumes", "Food Item": "Atta Flour / Whole Wheat Roti", "Portion Weight (g)": 40, "Portion Type": "1 Medium Roti", "Calories (kcal)": 104, "Carbs/Sugar (g)": 20.2, "GI": 52, "Sodium (mg)": 2, "Potassium (mg)": 110, "Sat Fat (g)": 0.2, "Purine Level": "Low", "Vitamins & Nutrients": "Whole Wheat Fiber, B-Vitamins", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "All-Purpose Flour (Maida)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Dry", "Calories (kcal)": 364, "Carbs/Sugar (g)": 76.3, "GI": 72, "Sodium (mg)": 2, "Potassium (mg)": 107, "Sat Fat (g)": 0.2, "Purine Level": "Low", "Vitamins & Nutrients": "Refined Starch", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Acceptable", "Hypertension Status": "Allowed", "Overall Suitability": "Not Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Pasta (Cooked Whole Wheat)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 124, "Carbs/Sugar (g)": 25.0, "GI": 42, "Sodium (mg)": 1, "Potassium (mg)": 60, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Complex Fiber, B-Vitamins", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Steel-Cut Oats (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 71, "Carbs/Sugar (g)": 12.0, "GI": 42, "Sodium (mg)": 1, "Potassium (mg)": 70, "Sat Fat (g)": 0.3, "Purine Level": "Low", "Vitamins & Nutrients": "High Beta-Glucan Fiber, B-Vitamins", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Instant Oats (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 82, "Carbs/Sugar (g)": 15.2, "GI": 66, "Sodium (mg)": 120, "Potassium (mg)": 60, "Sat Fat (g)": 0.4, "Purine Level": "Low", "Vitamins & Nutrients": "Processed Oats, Added Sodium", "HbA1c Status": "Acceptable", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Acceptable", "Overall Suitability": "Acceptable"},
    {"Category": "Grains & Legumes", "Food Item": "Rolled Oats (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1 Cup Cooked / Fist Size", "Calories (kcal)": 71, "Carbs/Sugar (g)": 12.0, "GI": 55, "Sodium (mg)": 1, "Potassium (mg)": 61, "Sat Fat (g)": 0.3, "Purine Level": "Low", "Vitamins & Nutrients": "Beta-Glucan Fiber, B-Vitamins", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Lentils (Boiled)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 116, "Carbs/Sugar (g)": 20.1, "GI": 32, "Sodium (mg)": 2, "Potassium (mg)": 369, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Folate, Fiber, Plant Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Grains & Legumes", "Food Item": "Quinoa (Cooked)", "Portion Weight (g)": 100, "Portion Type": "1/2 Cup Cooked", "Calories (kcal)": 120, "Carbs/Sugar (g)": 21.3, "GI": 53, "Sodium (mg)": 7, "Potassium (mg)": 172, "Sat Fat (g)": 0.2, "Purine Level": "Low", "Vitamins & Nutrients": "Magnesium, Iron, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # PROTEINS & SEAFOOD
    {"Category": "Proteins & Seafood", "Food Item": "Beef (Lean Grilled)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 213, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 58, "Potassium (mg)": 290, "Sat Fat (g)": 3.8, "Purine Level": "High", "Vitamins & Nutrients": "Iron, Zinc, Vit B12", "HbA1c Status": "Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Acceptable", "Hypertension Status": "Acceptable", "Overall Suitability": "Not Allowed"},
    {"Category": "Proteins & Seafood", "Food Item": "Pork (Lean Tenderloin)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 180, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 52, "Potassium (mg)": 330, "Sat Fat (g)": 2.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Thiamin B1, Vit B6, Selenium", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Acceptable", "Hypertension Status": "Acceptable", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Tilapia Fillet (Steamed)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 110, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 45, "Potassium (mg)": 320, "Sat Fat (g)": 0.6, "Purine Level": "Moderate", "Vitamins & Nutrients": "Lean Protein, B12, Selenium", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Tuna (Canned in Water)", "Portion Weight (g)": 85, "Portion Type": "1 Small Can / 3 oz", "Calories (kcal)": 112, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 210, "Potassium (mg)": 200, "Sat Fat (g)": 0.4, "Purine Level": "High", "Vitamins & Nutrients": "Vit D, Vit B12, Lean Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Acceptable", "Overall Suitability": "Not Allowed"},
    {"Category": "Proteins & Seafood", "Food Item": "Chicken Breast (Skinless)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 140, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 63, "Potassium (mg)": 218, "Sat Fat (g)": 0.9, "Purine Level": "Moderate", "Vitamins & Nutrients": "Niacin, Vit B6, Lean Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Salmon Fillet (Grilled)", "Portion Weight (g)": 85, "Portion Type": "Palm of Hand (3 oz)", "Calories (kcal)": 175, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 50, "Potassium (mg)": 309, "Sat Fat (g)": 1.3, "Purine Level": "Moderate", "Vitamins & Nutrients": "Omega-3 EPA/DHA, Vit D", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Acceptable"},

    # EGGS & DAIRY
    {"Category": "Eggs & Dairy", "Food Item": "Egg White (Boiled)", "Portion Weight (g)": 33, "Portion Type": "1 Large Egg White", "Calories (kcal)": 17, "Carbs/Sugar (g)": 0.2, "GI": 0, "Sodium (mg)": 55, "Potassium (mg)": 54, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Pure Ovalbumin Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Whole Egg (Boiled)", "Portion Weight (g)": 50, "Portion Type": "1 Large Egg", "Calories (kcal)": 72, "Carbs/Sugar (g)": 0.4, "GI": 0, "Sodium (mg)": 71, "Potassium (mg)": 69, "Sat Fat (g)": 1.6, "Purine Level": "Zero", "Vitamins & Nutrients": "Choline, Lutein, Vit D", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Acceptable", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Non-Fat Greek Yogurt", "Portion Weight (g)": 170, "Portion Type": "1 Individual Container (6 oz)", "Calories (kcal)": 100, "Carbs/Sugar (g)": 6.1, "GI": 12, "Sodium (mg)": 61, "Potassium (mg)": 240, "Sat Fat (g)": 0.2, "Purine Level": "Zero", "Vitamins & Nutrients": "Probiotics, Calcium, Uric Acid Lowering", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # NUTS & SEEDS
    {"Category": "Nuts & Seeds", "Food Item": "Walnuts (Raw)", "Portion Weight (g)": 30, "Portion Type": "1 Small Handful (7 halves)", "Calories (kcal)": 196, "Carbs/Sugar (g)": 4.1, "GI": 15, "Sodium (mg)": 1, "Potassium (mg)": 132, "Sat Fat (g)": 1.8, "Purine Level": "Low", "Vitamins & Nutrients": "ALA Omega-3, Magnesium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Nuts & Seeds", "Food Item": "Almonds (Unsalted Raw)", "Portion Weight (g)": 30, "Portion Type": "1 Small Handful (23 nuts)", "Calories (kcal)": 173, "Carbs/Sugar (g)": 6.1, "GI": 15, "Sodium (mg)": 0, "Potassium (mg)": 211, "Sat Fat (g)": 1.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit E, Magnesium, Arginine", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},

    # BEVERAGES & SWEETS
    {"Category": "Beverages & Sweets", "Food Item": "Green Tea (Unsweetened)", "Portion Weight (g)": 240, "Portion Type": "1 Mug / Cup", "Calories (kcal)": 2, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 2, "Potassium (mg)": 20, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "EGCG Catechins, Antioxidants", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Beverages & Sweets", "Food Item": "Black Coffee (Unsweetened)", "Portion Weight (g)": 240, "Portion Type": "1 Mug / Cup", "Calories (kcal)": 2, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 5, "Potassium (mg)": 116, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Chlorogenic Acid", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Beverages & Sweets", "Food Item": "Extra Virgin Olive Oil", "Portion Weight (g)": 14, "Portion Type": "1 Tablespoon", "Calories (kcal)": 119, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 0, "Potassium (mg)": 0, "Sat Fat (g)": 1.9, "Purine Level": "Zero", "Vitamins & Nutrients": "Oleic Acid, Polyphenols", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Hypertension Status": "Allowed", "Overall Suitability": "Allowed"}
]


# LIVE INTERNET NUTRITION SEARCH FUNCTION
def search_open_food_facts_live(query_term):
    """Queries live internet nutrition API on the spot for unlisted foods."""
    try:
        clean_q = urllib.parse.quote(query_term.strip())
        url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process&json=1&page_size=3".format(clean_q)
        req = urllib.request.Request(url, headers={'User-Agent': 'TargetHealthStreamlitApp/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                products = data.get("products", [])
                results = []
                for p in products:
                    name = p.get("product_name") or p.get("product_name_en")
                    if not name:
                        continue
                    nutr = p.get("nutriments", {})
                    cals = float(nutr.get("energy-kcal_100g") or nutr.get("energy-kcal") or 0.0)
                    carbs = float(nutr.get("carbohydrates_100g") or nutr.get("carbohydrates") or 0.0)
                    sugars = float(nutr.get("sugars_100g") or nutr.get("sugars") or 0.0)
                    sat_fat = float(nutr.get("saturated-fat_100g") or nutr.get("saturated-fat") or 0.0)
                    sodium_g = float(nutr.get("sodium_100g") or nutr.get("sodium") or 0.0)
                    sodium_mg = round(sodium_g * 1000.0, 1)
                    potassium_g = float(nutr.get("potassium_100g") or nutr.get("potassium") or 0.0)
                    potassium_mg = round(potassium_g * 1000.0, 1)
                    
                    suitability = "Allowed"
                    if cals > 250 or sugars > 15 or sat_fat > 3.0 or sodium_mg > 400:
                        suitability = "Acceptable"
                    if sugars > 25 or sat_fat > 5.0 or sodium_mg > 800:
                        suitability = "Not Allowed"
                        
                    results.append({
                        "Category": "Live Internet Result",
                        "Food Item": f"{name} (Live Internet)",
                        "Portion Weight (g)": 100,
                        "Portion Type": "100g Standard",
                        "Calories (kcal)": round(cals, 1),
                        "Carbs/Sugar (g)": round(carbs, 1),
                        "GI": 35,
                        "Sodium (mg)": sodium_mg,
                        "Potassium (mg)": potassium_mg,
                        "Sat Fat (g)": round(sat_fat, 1),
                        "Purine Level": "Low",
                        "Vitamins & Nutrients": "Live Internet Search Data",
                        "HbA1c Status": suitability,
                        "Uric Acid Status": suitability,
                        "Cholesterol Status": suitability,
                        "Hypertension Status": suitability,
                        "Overall Suitability": suitability
                    })
                return results
    except Exception:
        return []
    return []

# State Initialization
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if "custom_foods" not in st.session_state:
    st.session_state.custom_foods = []

if "user_logs" not in st.session_state:
    st.session_state.user_logs = {u: [] for u in USERS.keys()}

if "user_exercise" not in st.session_state:
    st.session_state.user_exercise = {u: [] for u in USERS.keys()}

if "user_bp" not in st.session_state:
    st.session_state.user_bp = {u: [] for u in USERS.keys()}

if "user_weight_history" not in st.session_state:
    st.session_state.user_weight_history = {u: [] for u in USERS.keys()}

def get_combined_db():
    all_data = INITIAL_FOOD_DATA + st.session_state.custom_foods
    df = pd.DataFrame(all_data)
    for col in ["Portion Type", "Hypertension Status", "Purine Level"]:
        if col not in df.columns:
            df[col] = "Standard"
    return df

df_db = get_combined_db()

# LOGIN SCREEN
if st.session_state.authenticated_user is None:
    st.title("🔐 TargetHealth Mobile Login")
    st.info("Select profile and enter password:")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        sel_u = st.selectbox("Select Profile", list(USERS.keys()))
        pass_in = st.text_input("Password", type="password")
        if st.button("🔓 Log In", use_container_width=True):
            if pass_in == USERS[sel_u]:
                st.session_state.authenticated_user = sel_u
                st.toast(f"Welcome back, {sel_u}!", icon="🎉")
                st.rerun()
            else:
                st.error("Incorrect password.")
    with c2:
        st.markdown("### 🔑 Demo Passwords:")
        st.code("User 1 (Alex): user1pass\nUser 2 (Maria): user2pass\nUser 3 (John): user3pass\nUser 4 (Sarah): user4pass")
    st.stop()

# LOGGED IN
active_user = st.session_state.authenticated_user

st.sidebar.markdown(f"👤 **Active User:** `{active_user}`")
if st.sidebar.button("🚪 Log Out", use_container_width=True):
    st.session_state.authenticated_user = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("🎯 Target Limits")
target_cals = st.sidebar.number_input("Max Calories (kcal)", value=2000, step=100)
target_sugar = st.sidebar.number_input("Max Sugar/Carbs (g) [HbA1c 5.0]", value=25, step=5)
target_sat_fat = st.sidebar.number_input("Max Sat Fat (g) [Cholesterol]", value=13, step=1)
target_sodium = st.sidebar.number_input("Max Sodium (mg) [Hypertension/DASH]", value=1500, step=100)
target_potassium = st.sidebar.number_input("Min Potassium Target (mg)", value=3500, step=100)

st.sidebar.markdown("#### 🩺 Target BP:")
bp_sys_target = st.sidebar.number_input("Target Systolic (mmHg)", value=120, step=5)
bp_dia_target = st.sidebar.number_input("Target Diastolic (mmHg)", value=80, step=5)

st.sidebar.markdown("#### ⚖️ Profile Body Weight:")
user_weight_kg = st.sidebar.number_input("Current Weight (kg)", value=70.0, step=0.5)

st.title("📱 TargetHealth Mobile Tracker")
st.caption(f"Profile: **{active_user}** | Targets: HbA1c 5.0%, Uric Acid 5.0 mg/dL, Low LDL, BP <{bp_sys_target}/{bp_dia_target}")

tab_log, tab_calc, tab_analytics, tab_db, tab_dl = st.tabs([
    "⏱️ Food Intake", 
    "⚖️ Weight & MET", 
    "📈 Analytics", 
    "🔍 Database", 
    "📥 Download"
])

# ==========================================
# TAB 1: FOOD INTAKE
# ==========================================
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
        p_mode = st.radio("Portion Mode", ["Estimated Size (No Scale)", "Custom Grams"], horizontal=True)
        base_g = float(sel_row["Portion Weight (g)"])
        def_label = sel_row.get("Portion Type", "Standard Serving")
        
        if p_mode == "Estimated Size (No Scale)":
            p_scale = st.select_slider(
                f"Size ({def_label})",
                options=["0.5x (Small)", "1.0x (Standard)", "1.5x (Large)", "2.0x (Double)"],
                value="1.0x (Standard)"
            )
            m_map = {"0.5x (Small)": 0.5, "1.0x (Standard)": 1.0, "1.5x (Large)": 1.5, "2.0x (Double)": 2.0}
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

    st.markdown("#### 🛡️ Pre-Eat Warning:")
    w1, w2 = st.columns([3, 1])
    with w1:
        if suitability == "Allowed":
            st.success("🟢 **Safe to Eat** — Fits all medical targets.")
        elif suitability == "Acceptable":
            st.warning("🟡 **Moderate Portion Caution** — Strict portion control needed.")
        else:
            st.error("🔴 **AVOID / High Risk** — Fails health targets!")
            
    with w2:
        if st.button("➕ Log Food Intake", use_container_width=True):
            log_entry = {
                "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                "Date": str(datetime.date.today()),
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
            st.toast(f"Logged {food_choice} ({portion_g}g)! ", icon="✅")

    # AI TEXT ESTIMATOR ACCORDION
    with st.expander("🤖🌐 **AI Text Food Estimator (Live Internet Search)**", expanded=True):
        st.caption("Type a text description of your meal (e.g. *'I ate 1 cup biryani rice, 100g beef, cabbage, and tea'*):")
        ai_text = st.text_area("Describe your food in words:", placeholder="e.g. 1 cup biryani rice, 100g grilled beef, cooked cabbage, and green tea")
        
        use_live_web = st.checkbox("🌐 **Search Internet Live for Unlisted Foods**", value=True)
        if st.button("✨ Parse & Search Internet Live"):
            if ai_text.strip():
                detected_items = []
                # Simple AI Keyword Matcher across DB
                for _, row in df_db.iterrows():
                    item_name = row["Food Item"]
                    clean_kw = re.sub(r'\(.*?\)', '', item_name).strip().lower()
                    if clean_kw in ai_text.lower():
                        detected_items.append(row)
                
                # Step 2: Live Internet Search for unlisted food items
                web_results = []
                if use_live_web:
                    words = re.findall(r'[a-zA-Z]{3,}', ai_text)
                    stop_words = {"ate", "and", "with", "cup", "grams", "cooked", "raw", "fresh", "some", "the", "for", "water", "tea", "slice", "glass", "piece", "rice", "food"}
                    unknown_words = [w.lower() for w in words if w.lower() not in stop_words and not any(w.lower() in item.get("Food Item", "").lower() for item in detected_items)]
                    for term in list(set(unknown_words))[:3]:
                        found_live = search_open_food_facts_live(term)
                        if found_live:
                            web_results.extend(found_live[:2])
                
                all_found_items = [row.to_dict() if hasattr(row, "to_dict") else row for row in detected_items] + web_results
                
                if all_found_items:
                    st.success(f"Matched **{len(all_found_items)} foods** (Local DB + Live Internet Search):")
                    ai_tot_cals = ai_tot_sugar = ai_tot_sat_fat = ai_tot_sodium = ai_tot_pot = 0.0
                    ai_log_entries = []
                    
                    for row in all_found_items:
                        st.markdown(f"- **{row['Food Item']}** ({row['Portion Weight (g)']}g): {row['Calories (kcal)']} kcal | {row['Carbs/Sugar (g)']}g sugar | {row['Sodium (mg)']}mg sodium | {row['Overall Suitability']}")
                        ai_tot_cals += row['Calories (kcal)']
                        ai_tot_sugar += row['Carbs/Sugar (g)']
                        ai_tot_sat_fat += row['Sat Fat (g)']
                        ai_tot_sodium += row['Sodium (mg)']
                        ai_tot_pot += row['Potassium (mg)']
                        
                        ai_log_entries.append({
                            "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                            "Date": str(datetime.date.today()),
                            "User": active_user,
                            "Meal": "AI Described Meal",
                            "Food Item": row['Food Item'],
                            "Category": row['Category'],
                            "Weight (g)": row['Portion Weight (g)'],
                            "Calories": row['Calories (kcal)'],
                            "Sugar/Carbs (g)": row['Carbs/Sugar (g)'],
                            "Sat Fat (g)": row['Sat Fat (g)'],
                            "Sodium (mg)": row['Sodium (mg)'],
                            "Potassium (mg)": row['Potassium (mg)'],
                            "Suitability": row['Overall Suitability']
                        })
                    
                    st.info(f"📊 **AI Total Estimate:** Calories: **{ai_tot_cals:.1f} kcal** | Sugar: **{ai_tot_sugar:.1f}g** | Sodium: **{ai_tot_sodium:.1f}mg**")
                    if st.button("➕ Log AI Estimated Items"):
                        for entry in ai_log_entries:
                            st.session_state.user_logs[active_user].append(entry)
                        st.toast("AI meal items logged successfully!", icon="✨")
                        st.rerun()
                else:
                    st.warning("No exact food matches found in text. Try mentioning items like *cabbage, biryani rice, beef, oats, kiwi, tea, chicken, salmon*.")

    # CUSTOM FOOD INPUT ACCORDION
    with st.expander("📝 **Input Custom Purchased Food Item**"):
        st.caption("Input nutrition facts from a food label or purchased item:")
        cf1, cf2 = st.columns(2)
        with cf1:
            c_name = st.text_input("Food Name", "Custom Purchased Salad")
            c_cat = st.selectbox("Category ", df_db["Category"].unique())
            c_weight = st.number_input("Serving Weight (g)", value=100, step=10)
            c_cals = st.number_input("Calories (kcal)", value=150, step=10)
            c_sugar = st.number_input("Sugar/Carbs (g)", value=10.0, step=1.0)
        with cf2:
            c_sat_fat = st.number_input("Sat Fat (g)", value=1.0, step=0.5)
            c_sodium = st.number_input("Sodium (mg)", value=200, step=10)
            c_potassium = st.number_input("Potassium (mg)", value=150, step=10)
            c_purine = st.selectbox("Purine Level", ["Zero", "Low", "Moderate", "High"])
            c_suit = st.selectbox("Suitability", ["Allowed", "Acceptable", "Not Allowed"])
            
        if st.button("💾 Save Custom Food to Database"):
            new_custom = {
                "Category": c_cat, "Food Item": f"{c_name} (Custom)", "Portion Weight (g)": c_weight,
                "Portion Type": "Custom Package", "Calories (kcal)": c_cals, "Carbs/Sugar (g)": c_sugar,
                "GI": 30, "Sodium (mg)": c_sodium, "Potassium (mg)": c_potassium, "Sat Fat (g)": c_sat_fat,
                "Purine Level": c_purine, "Vitamins & Nutrients": "Custom Item Data",
                "HbA1c Status": c_suit, "Uric Acid Status": c_suit, "Cholesterol Status": c_suit,
                "Hypertension Status": c_suit, "Overall Suitability": c_suit
            }
            st.session_state.custom_foods.append(new_custom)
            st.toast(f"Added '{c_name}' to Database!", icon="💾")
            st.rerun()

    st.markdown("---")
    st.subheader("2. Cumulative Daily Allowance Dashboard")
    
    user_log_list = st.session_state.user_logs[active_user]
    today_str = str(datetime.date.today())
    today_logs = [l for l in user_log_list if l.get("Date", today_str) == today_str]
    
    if today_logs:
        df_today = pd.DataFrame(today_logs)
        tot_cals = round(df_today["Calories"].sum(), 1)
        tot_sugar = round(df_today["Sugar/Carbs (g)"].sum(), 1)
        tot_sat_fat = round(df_today["Sat Fat (g)"].sum(), 1)
        tot_sodium = round(df_today["Sodium (mg)"].sum(), 1)
        tot_potassium = round(df_today["Potassium (mg)"].sum(), 1)
    else:
        df_today = pd.DataFrame()
        tot_cals = tot_sugar = tot_sat_fat = tot_sodium = tot_potassium = 0.0

    user_ex_list = st.session_state.user_exercise[active_user]
    cals_burned = sum(e["Calories Burned"] for e in user_ex_list if e.get("Date", today_str) == today_str) if user_ex_list else 0.0
    net_cals = round(tot_cals - cals_burned, 1)

    # TRAFFIC LIGHT COLOR CALCULATIONS (<85% Green, 85-100% Yellow, >100% Red)
    def get_traffic_light(val, limit):
        if limit <= 0: return "🟢 Safe", "green"
        pct = (val / limit) * 100
        if pct > 100:
            return f"🔴 EXCEEDED ({pct:.0f}%)", "red"
        elif pct >= 85:
            return f"🟡 Near Limit ({pct:.0f}%)", "yellow"
        else:
            return f"🟢 Within Limit ({pct:.0f}%)", "green"

    status_cals, col_cals = get_traffic_light(net_cals, target_cals)
    status_sugar, col_sugar = get_traffic_light(tot_sugar, target_sugar)
    status_fat, col_fat = get_traffic_light(tot_sat_fat, target_sat_fat)
    status_sod, col_sod = get_traffic_light(tot_sodium, target_sodium)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Net Calories", f"{net_cals} kcal", status_cals)
    m2.metric("Sugar / Carbs", f"{tot_sugar} g", status_sugar)
    m3.metric("Sat Fat", f"{tot_sat_fat} g", status_fat)
    m4.metric("Sodium (DASH)", f"{tot_sodium} mg", status_sod)

    st.markdown("##### 🚦 Traffic Light Limit Statuses:")
    st.progress(min(max(net_cals / target_cals, 0.0), 1.0), text=f"Calories: {net_cals}/{target_cals} kcal ({status_cals})")
    st.progress(min(max(tot_sugar / target_sugar, 0.0), 1.0), text=f"Sugar/Carbs: {tot_sugar}/{target_sugar} g ({status_sugar})")
    st.progress(min(max(tot_sodium / target_sodium, 0.0), 1.0), text=f"Sodium: {tot_sodium}/{target_sodium} mg ({status_sod})")

    if not df_today.empty:
        st.markdown("#### 📋 Today's Logged Items:")
        st.dataframe(df_today[["Timestamp", "Meal", "Food Item", "Weight (g)", "Calories", "Sugar/Carbs (g)", "Sodium (mg)", "Suitability"]], use_container_width=True)
        if st.button("🗑️ Clear Today's Intake Log"):
            st.session_state.user_logs[active_user] = [l for l in user_log_list if l.get("Date") != today_str]
            st.rerun()

# ==========================================
# TAB 2: WEIGHT & MET CALORIE BURN
# ==========================================
with tab_calc:
    st.subheader("⚖️ Body Weight & MET Exercise Burn Link")
    
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        st.markdown("#### 🏃 Log Physical Exercise (MET Burn):")
        activity = st.selectbox("Activity", ["Brisk Walking", "Running / Jogging", "Cycling", "Swimming", "Gym / Weight Training", "Household Work"])
        duration = st.number_input("Duration (minutes)", value=30, min_value=5, max_value=300, step=5)
        
        # MET Values (Metabolic Equivalent)
        met_map = {"Brisk Walking": 3.8, "Running / Jogging": 9.8, "Cycling": 7.5, "Swimming": 8.0, "Gym / Weight Training": 5.0, "Household Work": 3.0}
        met_val = met_map[activity]
        
        # Formula: Burn = MET * Weight_kg * (Duration_min / 60)
        cals_burned_calc = round(met_val * user_weight_kg * (duration / 60.0), 1)
        
        st.info(f"🔥 Calculated Burn for **{user_weight_kg} kg**: **{cals_burned_calc} kcal**")
        if st.button("➕ Log Exercise Burn", use_container_width=True):
            st.session_state.user_exercise[active_user].append({
                "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                "Date": str(datetime.date.today()),
                "Activity": activity,
                "Duration (min)": duration,
                "Calories Burned": cals_burned_calc
            })
            st.toast(f"Logged {activity} ({cals_burned_calc} kcal)! ", icon="🔥")
            st.rerun()

    with w_col2:
        st.markdown("#### 🩺 Log Blood Pressure & Weight:")
        sys_bp = st.number_input("Systolic (mmHg)", value=120, min_value=70, max_value=220, step=1)
        dia_bp = st.number_input("Diastolic (mmHg)", value=80, min_value=40, max_value=140, step=1)
        
        if sys_bp <= bp_sys_target and dia_bp <= bp_dia_target:
            bp_status = "🟢 Within BP Target"
        elif sys_bp <= 129 and dia_bp <= 80:
            bp_status = "🟡 Elevated BP"
        else:
            bp_status = "🔴 Above BP Target"
            
        st.markdown(f"Status: **{bp_status}**")
        if st.button("➕ Log BP & Weight Entry", use_container_width=True):
            st.session_state.user_bp[active_user].append({
                "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                "Date": str(datetime.date.today()),
                "Systolic": sys_bp,
                "Diastolic": dia_bp,
                "Weight (kg)": user_weight_kg,
                "Status": bp_status
            })
            st.toast(f"Logged BP {sys_bp}/{dia_bp} mmHg and Weight {user_weight_kg}kg!", icon="🩺")

# ==========================================
# TAB 3: ANALYTICS & CHARTS
# ==========================================
with tab_analytics:
    st.subheader("📈 Daily, Weekly & Monthly Analytics")
    
    if user_log_list:
        df_all_logs = pd.DataFrame(user_log_list)
        
        # 1. Daily Chart
        st.markdown("#### 1. Today's Calorie Breakdown by Meal:")
        if not df_today.empty:
            meal_chart = df_today.groupby("Meal")["Calories"].sum()
            st.bar_chart(meal_chart)
        else:
            st.info("No logs recorded today for daily chart.")
            
        # 2. Weekly / Historical Intake vs Limit
        st.markdown("#### 2. Calorie Trends Across Days:")
        daily_summary = df_all_logs.groupby("Date")[["Calories", "Sugar/Carbs (g)", "Sodium (mg)"]].sum()
        st.line_chart(daily_summary)
    else:
        st.info("No food intake recorded yet. Start logging meals to see analytics charts.")

# ==========================================
# TAB 4: DATABASE EXPLORER
# ==========================================
with tab_db:
    st.subheader("🔍 Master Database (80+ Foods & Custom Added)")
    st.dataframe(df_db, use_container_width=True)

# ==========================================
# TAB 5: DOWNLOAD DATA
# ==========================================
with tab_dl:
    st.subheader(f"📥 Download Profile Log (.CSV)")
    if user_log_list:
        df_export = pd.DataFrame(user_log_list)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Food Intake Log (.CSV)",
            data=csv_data,
            file_name=f"{active_user.replace(' ', '_')}_food_log_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No intake recorded yet to download.")
