import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TargetHealth Food Tracker",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- EMBEDDED MEDICAL FOOD DATABASE ---
FOOD_DATA = [
    # Vegetables & Greens
    {"Category": "Vegetables & Greens", "Food Item": "Spinach (Raw)", "Portion Weight (g)": 100, "Calories (kcal)": 23, "Carbs/Sugar (g)": 3.6, "GI": 15, "Sodium (mg)": 79, "Potassium (mg)": 558, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Vit A, C, K, Folate, Iron", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Broccoli (Steamed)", "Portion Weight (g)": 100, "Calories (kcal)": 35, "Carbs/Sugar (g)": 7.2, "GI": 15, "Sodium (mg)": 33, "Potassium (mg)": 316, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Vit C, K, Fiber, Sulforaphane", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Cucumber (With Peel)", "Portion Weight (g)": 100, "Calories (kcal)": 15, "Carbs/Sugar (g)": 3.6, "GI": 15, "Sodium (mg)": 2, "Potassium (mg)": 147, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit K, Water, Potassium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Vegetables & Greens", "Food Item": "Cauliflower (Boiled)", "Portion Weight (g)": 100, "Calories (kcal)": 23, "Carbs/Sugar (g)": 4.1, "GI": 15, "Sodium (mg)": 15, "Potassium (mg)": 142, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Vit C, K, Choline", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},

    # Fruits & Berries
    {"Category": "Fruits & Berries", "Food Item": "Tart Cherries (Fresh)", "Portion Weight (g)": 100, "Calories (kcal)": 50, "Carbs/Sugar (g)": 12.2, "GI": 22, "Sodium (mg)": 0, "Potassium (mg)": 173, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Anthocyanins, Vit C", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Blueberries (Fresh)", "Portion Weight (g)": 100, "Calories (kcal)": 57, "Carbs/Sugar (g)": 14.5, "GI": 53, "Sodium (mg)": 1, "Potassium (mg)": 77, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Vit C, K, Manganese, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Green Apple (Sliced)", "Portion Weight (g)": 100, "Calories (kcal)": 52, "Carbs/Sugar (g)": 13.8, "GI": 36, "Sodium (mg)": 1, "Potassium (mg)": 107, "Sat Fat (g)": 0.1, "Purine Level": "Low", "Vitamins & Nutrients": "Pectin Fiber, Vit C", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Fruits & Berries", "Food Item": "Watermelon", "Portion Weight (g)": 100, "Calories (kcal)": 30, "Carbs/Sugar (g)": 7.5, "GI": 72, "Sodium (mg)": 1, "Potassium (mg)": 112, "Sat Fat (g)": 0.0, "Purine Level": "Low", "Vitamins & Nutrients": "Lycopene, Vit A, C", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Not Allowed"},

    # Grains & Legumes
    {"Category": "Grains & Legumes", "Food Item": "Rolled Oats (Cooked)", "Portion Weight (g)": 100, "Calories (kcal)": 71, "Carbs/Sugar (g)": 12.0, "GI": 55, "Sodium (mg)": 1, "Potassium (mg)": 61, "Sat Fat (g)": 0.3, "Purine Level": "Low", "Vitamins & Nutrients": "Beta-Glucan Fiber, B-Vitamins", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "Lentils (Boiled)", "Portion Weight (g)": 100, "Calories (kcal)": 116, "Carbs/Sugar (g)": 20.1, "GI": 32, "Sodium (mg)": 2, "Potassium (mg)": 369, "Sat Fat (g)": 0.1, "Purine Level": "Moderate", "Vitamins & Nutrients": "Folate, Fiber, Plant Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Grains & Legumes", "Food Item": "Quinoa (Cooked)", "Portion Weight (g)": 100, "Calories (kcal)": 120, "Carbs/Sugar (g)": 21.3, "GI": 53, "Sodium (mg)": 7, "Potassium (mg)": 172, "Sat Fat (g)": 0.2, "Purine Level": "Low", "Vitamins & Nutrients": "Magnesium, Iron, Fiber", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Grains & Legumes", "Food Item": "White Bread", "Portion Weight (g)": 100, "Calories (kcal)": 265, "Carbs/Sugar (g)": 49.0, "GI": 75, "Sodium (mg)": 490, "Potassium (mg)": 115, "Sat Fat (g)": 0.7, "Purine Level": "Low", "Vitamins & Nutrients": "Refined Starch", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Acceptable", "Overall Suitability": "Not Allowed"},

    # Proteins & Seafood
    {"Category": "Proteins & Seafood", "Food Item": "Chicken Breast (Skinless)", "Portion Weight (g)": 100, "Calories (kcal)": 165, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 74, "Potassium (mg)": 256, "Sat Fat (g)": 1.0, "Purine Level": "Moderate", "Vitamins & Nutrients": "Niacin, Vit B6, Lean Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Salmon Fillet (Grilled)", "Portion Weight (g)": 100, "Calories (kcal)": 206, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 59, "Potassium (mg)": 363, "Sat Fat (g)": 1.5, "Purine Level": "Moderate", "Vitamins & Nutrients": "Omega-3 EPA/DHA, Vit D", "HbA1c Status": "Allowed", "Uric Acid Status": "Acceptable", "Cholesterol Status": "Allowed", "Overall Suitability": "Acceptable"},
    {"Category": "Proteins & Seafood", "Food Item": "Organ Meats (Beef Liver)", "Portion Weight (g)": 100, "Calories (kcal)": 175, "Carbs/Sugar (g)": 5.2, "GI": 0, "Sodium (mg)": 69, "Potassium (mg)": 331, "Sat Fat (g)": 1.8, "Purine Level": "Very High", "Vitamins & Nutrients": "Vit A, B12, Iron (HIGH PURINE)", "HbA1c Status": "Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Not Allowed", "Overall Suitability": "Not Allowed"},
    {"Category": "Proteins & Seafood", "Food Item": "Sardines (In Water)", "Portion Weight (g)": 100, "Calories (kcal)": 208, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 307, "Potassium (mg)": 397, "Sat Fat (g)": 1.5, "Purine Level": "High", "Vitamins & Nutrients": "Calcium, Vit D, Omega-3", "HbA1c Status": "Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Not Allowed"},

    # Eggs & Dairy
    {"Category": "Eggs & Dairy", "Food Item": "Egg White (Boiled)", "Portion Weight (g)": 100, "Calories (kcal)": 52, "Carbs/Sugar (g)": 0.7, "GI": 0, "Sodium (mg)": 166, "Potassium (mg)": 163, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "Pure Ovalbumin Protein", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Non-Fat Greek Yogurt", "Portion Weight (g)": 100, "Calories (kcal)": 59, "Carbs/Sugar (g)": 3.6, "GI": 12, "Sodium (mg)": 36, "Potassium (mg)": 141, "Sat Fat (g)": 0.1, "Purine Level": "Zero", "Vitamins & Nutrients": "Probiotics, Calcium, Uric Acid Lowering", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Eggs & Dairy", "Food Item": "Whole Milk (3.25%)", "Portion Weight (g)": 100, "Calories (kcal)": 61, "Carbs/Sugar (g)": 4.8, "GI": 39, "Sodium (mg)": 43, "Potassium (mg)": 132, "Sat Fat (g)": 1.9, "Purine Level": "Zero", "Vitamins & Nutrients": "Calcium, Vit D", "HbA1c Status": "Acceptable", "Uric Acid Status": "Allowed", "Cholesterol Status": "Not Allowed", "Overall Suitability": "Not Allowed"},

    # Nuts & Seeds
    {"Category": "Nuts & Seeds", "Food Item": "Walnuts (Raw)", "Portion Weight (g)": 100, "Calories (kcal)": 654, "Carbs/Sugar (g)": 13.7, "GI": 15, "Sodium (mg)": 2, "Potassium (mg)": 441, "Sat Fat (g)": 6.1, "Purine Level": "Low", "Vitamins & Nutrients": "ALA Omega-3, Magnesium", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Nuts & Seeds", "Food Item": "Chia Seeds (Dry)", "Portion Weight (g)": 100, "Calories (kcal)": 486, "Carbs/Sugar (g)": 42.1, "GI": 1, "Sodium (mg)": 16, "Potassium (mg)": 407, "Sat Fat (g)": 3.3, "Purine Level": "Low", "Vitamins & Nutrients": "Soluble Fiber, Calcium, ALA", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},

    # Beverages & Sweets
    {"Category": "Beverages & Sweets", "Food Item": "Green Tea (Unsweetened)", "Portion Weight (g)": 100, "Calories (kcal)": 1, "Carbs/Sugar (g)": 0.0, "GI": 0, "Sodium (mg)": 1, "Potassium (mg)": 8, "Sat Fat (g)": 0.0, "Purine Level": "Zero", "Vitamins & Nutrients": "EGCG Catechins, Antioxidants", "HbA1c Status": "Allowed", "Uric Acid Status": "Allowed", "Cholesterol Status": "Allowed", "Overall Suitability": "Allowed"},
    {"Category": "Beverages & Sweets", "Food Item": "Regular Soda (Sweetened)", "Portion Weight (g)": 100, "Calories (kcal)": 38, "Carbs/Sugar (g)": 10.6, "GI": 63, "Sodium (mg)": 4, "Potassium (mg)": 2, "Sat Fat (g)": 0.0, "Purine Level": "High (HFCS)", "Vitamins & Nutrients": "High Fructose Corn Syrup", "HbA1c Status": "Not Allowed", "Uric Acid Status": "Not Allowed", "Cholesterol Status": "Not Allowed", "Overall Suitability": "Not Allowed"}
]

@st.cache_data
def load_database():
    return pd.DataFrame(FOOD_DATA)

# --- INITIALIZE SESSION STATE ---
if "log_data" not in st.session_state:
    st.session_state.log_data = []

df_db = load_database()

# --- HEADER & SIDEBAR SETTINGS ---
st.title("🥗 TargetHealth: Triple-Target Food & Metabolic Logger")
st.markdown("""
**Personalized Metabolic Tracker** optimized for three simultaneous health targets:
1. **HbA1c Target 5.0%** (Glycemic Control / Blood Sugar Spike Avoidance)
2. **Uric Acid Target 5.0 mg/dL** (Purine & Fructose Management)
3. **Low LDL Cholesterol Target** (Saturated Fat & Fiber Optimization)
""")

st.sidebar.header("🎯 Daily Ceiling & Target Limits")
st.sidebar.markdown("Customize your daily allowances based on physician recommendations:")

target_calories = st.sidebar.number_input("Max Daily Calories (kcal)", value=2000, step=100)
target_sugar = st.sidebar.number_input("Max Added Sugar/Carbs (g)", value=25, step=5)
target_sat_fat = st.sidebar.number_input("Max Saturated Fat (g)", value=13, step=1)
target_sodium = st.sidebar.number_input("Max Sodium (mg)", value=1500, step=100)
target_potassium = st.sidebar.number_input("Min Potassium Target (mg)", value=3500, step=100)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Medical Guidance:** Saturated fat is capped at <6% of total calories (AHA), sugar is restricted to prevent glycemic volatility, and purines/HFCS are strictly filtered to keep uric acid at ~5.0 mg/dL.")

# --- NAVIGATION TABS ---
tab_log, tab_db, tab_guidance = st.tabs([
    "⏱️ Pre-Eat Counter & Food Logger", 
    "🔍 Food Database Explorer", 
    "📚 Clinical Rationale & Guidelines"
])

# ==========================================
# TAB 1: PRE-EAT COUNTER & FOOD LOGGER
# ==========================================
with tab_log:
    st.subheader("1. Pre-Eat Safety Check & Logger")
    
    col_input1, col_input2, col_input3 = st.columns([2, 2, 1])
    
    with col_input1:
        category_choice = st.selectbox("Select Category", df_db["Category"].unique())
        sub_df = df_db[df_db["Category"] == category_choice]
        food_choice = st.selectbox("Select Food Item", sub_df["Food Item"].unique())
    
    selected_row = sub_df[sub_df["Food Item"] == food_choice].iloc[0]
    
    with col_input2:
        meal_type = st.selectbox("Meal / Time", ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner", "Late Snack"])
        portion_g = st.number_input("Portion Weight (grams)", value=int(selected_row["Portion Weight (g)"]), min_value=1, max_value=2000, step=10)
    
    # Calculate serving multiplier
    mult = portion_g / float(selected_row["Portion Weight (g)"])
    
    item_cals = round(selected_row["Calories (kcal)"] * mult, 1)
    item_sugar = round(selected_row["Carbs/Sugar (g)"] * mult, 1)
    item_sat_fat = round(selected_row["Sat Fat (g)"] * mult, 1)
    item_sodium = round(selected_row["Sodium (mg)"] * mult, 1)
    item_potassium = round(selected_row["Potassium (mg)"] * mult, 1)
    suitability = selected_row["Overall Suitability"]
    
    with col_input3:
        st.markdown("**Safety Warning:**")
        if suitability == "Allowed":
            st.success("🟢 Safe to Eat\n\nFits all 3 target guidelines.")
        elif suitability == "Acceptable":
            st.warning("🟡 Moderate Portion\n\nAcceptable with caution.")
        else:
            st.error("🔴 AVOID - High Risk\n\nFails 1+ health targets!")
            
        if st.button("➕ Log Food Intake", use_container_width=True):
            log_entry = {
                "Timestamp": datetime.datetime.now().strftime("%H:%M"),
                "Meal": meal_type,
                "Food Item": food_choice,
                "Category": category_choice,
                "Weight (g)": portion_g,
                "Calories": item_cals,
                "Sugar/Carbs (g)": item_sugar,
                "Sat Fat (g)": item_sat_fat,
                "Sodium (mg)": item_sodium,
                "Potassium (mg)": item_potassium,
                "Suitability": suitability
            }
            st.session_state.log_data.append(log_entry)
            st.toast(f"Logged {food_choice} ({portion_g}g)!", icon="✅")

    st.markdown("---")
    st.subheader("2. Daily Cumulative Allowance Dashboard")
    
    # Compute totals from session state log
    if st.session_state.log_data:
        df_log = pd.DataFrame(st.session_state.log_data)
        tot_cals = round(df_log["Calories"].sum(), 1)
        tot_sugar = round(df_log["Sugar/Carbs (g)"].sum(), 1)
        tot_sat_fat = round(df_log["Sat Fat (g)"].sum(), 1)
        tot_sodium = round(df_log["Sodium (mg)"].sum(), 1)
        tot_potassium = round(df_log["Potassium (mg)"].sum(), 1)
    else:
        df_log = pd.DataFrame()
        tot_cals = tot_sugar = tot_sat_fat = tot_sodium = tot_potassium = 0.0

    rem_cals = target_calories - tot_cals
    rem_sugar = target_sugar - tot_sugar
    rem_sat_fat = target_sat_fat - tot_sat_fat
    rem_sodium = target_sodium - tot_sodium

    m1, m2, m3, m4, m5 = st.columns(5)
    
    m1.metric("Calories Intake", f"{tot_cals} kcal", f"{rem_cals} kcal left", delta_color="normal" if rem_cals>=0 else "inverse")
    m2.metric("Sugar / Carbs", f"{tot_sugar} g", f"{rem_sugar} g left", delta_color="normal" if rem_sugar>=0 else "inverse")
    m3.metric("Saturated Fat", f"{tot_sat_fat} g", f"{rem_sat_fat} g left", delta_color="normal" if rem_sat_fat>=0 else "inverse")
    m4.metric("Sodium Intake", f"{tot_sodium} mg", f"{rem_sodium} mg left", delta_color="normal" if rem_sodium>=0 else "inverse")
    m5.metric("Potassium Achieved", f"{tot_potassium} mg", f"Goal: {target_potassium} mg")

    # Progress bars
    st.caption("📈 **Daily Cap Progress:**")
    st.progress(min(tot_cals / target_calories, 1.0), text=f"Calories ({tot_cals}/{target_calories} kcal)")
    st.progress(min(tot_sat_fat / target_sat_fat, 1.0), text=f"Saturated Fat ({tot_sat_fat}/{target_sat_fat} g)")

    st.markdown("---")
    st.subheader("3. Logged Food Summary")
    
    if not df_log.empty:
        st.dataframe(df_log, use_container_width=True)
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("🗑️ Clear Today's Log"):
                st.session_state.log_data = []
                st.rerun()
    else:
        st.info("No food logged today yet. Select an item above and click 'Log Food Intake' to track.")

# ==========================================
# TAB 2: FOOD DATABASE EXPLORER
# ==========================================
with tab_db:
    st.subheader("Nutritional Reference & Suitability Database")
    
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        cat_filter = st.multiselect("Filter Category", df_db["Category"].unique(), default=df_db["Category"].unique())
    with f_col2:
        suit_filter = st.multiselect("Filter Suitability Tag", df_db["Overall Suitability"].unique(), default=df_db["Overall Suitability"].unique())
    with f_col3:
        search_term = st.text_input("Search Food Item", "")
        
    filtered_df = df_db[
        (df_db["Category"].isin(cat_filter)) & 
        (df_db["Overall Suitability"].isin(suit_filter)) &
        (df_db["Food Item"].str.contains(search_term, case=False, na=False))
    ]
    
    st.dataframe(filtered_df, use_container_width=True)

# ==========================================
# TAB 3: CLINICAL RATIONALE & GUIDELINES
# ==========================================
with tab_guidance:
    st.subheader("Medical Standards for Combined Targets")
    st.markdown("""
    ### 🩸 1. HbA1c 5.0% Target (Glycemic Control & Spike Avoidance)
    *   **Low Glycemic Index (GI < 55):** Foods high in fiber (e.g., oats, legumes, chia seeds) slow glucose absorption and prevent blood sugar spikes.
    *   **Refined Carbohydrate & HFCS Restriction:** Sugary beverages, white bread, and added sugars cause sharp glycemic surges and contribute to systemic insulin resistance.

    ### 🍗 2. Uric Acid 5.0 mg/dL Target (Purine Management)
    *   **Strict Purine Limits:** Avoid organ meats, shellfish, and small oily fish which breakdown directly into uric acid.
    *   **Zero High-Fructose Corn Syrup (HFCS):** Fructose accelerates ATP breakdown in the liver, directly increasing uric acid production.
    *   **Beneficial Protective Foods:** Non-fat dairy (Greek yogurt) and tart cherries enhance renal uric acid clearance.

    ### ❤️ 3. Low LDL Cholesterol Target (Cardiovascular Health)
    *   **Saturated Fat Limit (<6% Calories):** Capped at ~13g/day on a 2,000 kcal diet per American Heart Association (AHA) guidelines.
    *   **Soluble Fiber Boost:** Beta-glucan from oats and pectin from apples bind bile acids in the gut, actively reducing serum LDL cholesterol.
    """)
