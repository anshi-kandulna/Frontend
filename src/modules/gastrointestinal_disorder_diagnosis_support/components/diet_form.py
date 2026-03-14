# components/diet_form.py

import streamlit as st
from datetime import datetime, time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.diet_service import DietService

def diet_form():
    """
    Collect dietary data for correlation with symptoms
    """
    st.header("Dietary Tracking")
    
    diet_data = {}
    
    # 1. Date and Time - Combined into datetime
    st.subheader("When Did You Eat? *")
    col1, col2 = st.columns(2)
    with col1:
        meal_date = st.date_input("Date")
    with col2:
        meal_time = st.time_input("Time", value=time(12, 0))
    
    # Combine date and time into datetime
    if meal_date and meal_time:
        diet_data['meal_time'] = datetime.combine(meal_date, meal_time).isoformat()
    
    # 3. Food Items
    # st.subheader("Food Items")
    # diet_data['main_food'] = st.text_input("Main Food Item")  
    
    # 4. Common Food Categories to Check
    st.subheader("Food Categories *")
    food_categories = {
        "Spicy": st.checkbox("Spicy/Peppers", key="food_spicy"),
        "Dairy": st.checkbox("Dairy Products", key="food_dairy"),
        "Fatty/Oily": st.checkbox("Fatty/Oily", key="food_fatty"),
        "Acidic": st.checkbox("Acidic (Citrus, Tomato)", key="food_acidic"),
        "High Fiber": st.checkbox("High Fiber", key="food_fiber"),
        "Gluten": st.checkbox("Gluten", key="food_gluten"),
        "Caffeine": st.checkbox("Caffeine", key="food_caffeine"),
        "Alcohol": st.checkbox("Alcohol", key="food_alcohol"),
        "Raw/Uncooked": st.checkbox("Raw/Uncooked", key="food_raw"),
    }
    diet_data['food_category'] = [k for k, v in food_categories.items() if v]
    
    # 5. Portion Size
    st.subheader("Portion Size")
    diet_data['portion_size'] = st.selectbox(
        "Portion Size",
        ["Small", "Medium", "Large", "Extra Large"],
        index=None,
        placeholder="Select a portion size"
    )
    
    # 6. Ingredients/Allergens
    st.subheader("Allergens")
    ingredients = st.multiselect(
        "Select ingredients (if known)",
        [
            "Milk", "Eggs", "Peanuts", "Tree Nuts", "Fish", 
            "Shellfish", "Soy", "Wheat", "Sesame", "Other"
        ]
    )
    diet_data['allergens'] = ingredients
    
    # 7. Symptoms After Eating
    st.subheader("Symptoms After Eating")
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
    
    diet_data['symptoms_after_eating'] = symptoms_after
    
    
    # 9. Additional Notes
    # st.subheader("Additional Notes")
    # diet_data['notes'] = st.text_area("Any additional notes about the meal")
    
    # 10. Submit Button
    if st.button("Record Meal"):
        errors = []
        
        # Validate required fields (with *)
        if not diet_data.get('meal_time'):
            errors.append("❌ Please select date and time")
        
        if not diet_data.get('food_category'):
            errors.append("❌ Please select at least one food category")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            patient_id = st.session_state.get("patient_id", "patient_001")
            response = DietService.submit_diet_data(patient_id, diet_data)
            
            if response.get('success'):
                st.success(f"✓ Meal recorded! ID: {response.get('id')}")
            else:
                st.error(f"Error: {response.get('error', 'Unknown error')}")
    
    return None


diet_form()