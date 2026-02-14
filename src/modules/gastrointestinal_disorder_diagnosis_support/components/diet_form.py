# components/diet_form.py

import streamlit as st
from datetime import datetime

def diet_form():
    """
    Collect dietary data for correlation with symptoms
    """
    st.header("Dietary Tracking")
    
    diet_data = {}
    
    # 1. Date and Time
    st.subheader("When Did You Eat?")
    col1, col2 = st.columns(2)
    with col1:
        diet_data['date'] = st.date_input("Date")
    with col2:
        diet_data['time'] = st.time_input("Time")
    
    # 3. Food Items
    st.subheader("Food Items")
    diet_data['main_food'] = st.text_input("Main Food Item")  
    
    # 4. Common Food Categories to Check
    st.subheader("Food Categories")
    food_categories = {
        "Spicy": st.checkbox("Spicy/Peppers"),
        "Dairy": st.checkbox("Dairy Products"),
        "Fatty/Oily": st.checkbox("Fatty/Oily"),
        "Acidic": st.checkbox("Acidic (Citrus, Tomato)"),
        "High Fiber": st.checkbox("High Fiber"),
        "Gluten": st.checkbox("Gluten"),
        "Caffeine": st.checkbox("Caffeine"),
        "Alcohol": st.checkbox("Alcohol"),
        "Raw/Uncooked": st.checkbox("Raw/Uncooked"),
    }
    diet_data['categories'] = [k for k, v in food_categories.items() if v]
    
    # 5. Portion Size
    st.subheader("Portion Size")
    diet_data['portion_size'] = st.selectbox(
        "Portion Size",
        ["Small", "Medium", "Large", "Extra Large"]
    )
    
    # 6. Ingredients/Allergens
    st.subheader("Ingredients & Allergens")
    ingredients = st.multiselect(
        "Select ingredients (if known)",
        [
            "Milk", "Eggs", "Peanuts", "Tree Nuts", "Fish", 
            "Shellfish", "Soy", "Wheat", "Sesame", "Other"
        ]
    )
    diet_data['ingredients'] = ingredients
    
    # 7. Symptoms After Eating
    st.subheader("Symptoms After Eating (Optional)")
    symptoms_after = []
    symptoms_list = [
        "Bloating",
        "Gas",
        "Stomach Pain",
        "Nausea",
        "Diarrhea",
        "Heartburn",
        "None"
    ]
    for symptom in symptoms_list:
        if st.checkbox(f"  {symptom}", key=f"symptom_{symptom}"):
            symptoms_after.append(symptom)
    
    diet_data['symptoms_after'] = symptoms_after
    
    # 8. Time to Symptoms
    if symptoms_after and "None" not in symptoms_after:
        st.subheader("Time to Symptom Onset")
        diet_data['time_to_symptom'] = st.selectbox(
            "How long after eating did symptoms start?",
            ["Immediately", "15-30 minutes", "30-60 minutes", "1-2 hours", "2-4 hours", "Later"]
        )
    
    # 9. Additional Notes
    st.subheader("Additional Notes")
    diet_data['notes'] = st.text_area("Any additional notes about the meal")
    
    # 10. Submit Button
    if st.button("Record Meal"):
        if diet_data['main_food']:
            return diet_data
        else:
            st.error("Please enter a food item!")
    
    return None


diet_form()