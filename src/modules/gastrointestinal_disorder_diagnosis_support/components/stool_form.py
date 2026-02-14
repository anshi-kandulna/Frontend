# components/stool_form.py

import streamlit as st
from datetime import datetime

def stool_form():
    """
    Collect stool characteristic data for GI disorder analysis
    Uses Bristol Stool Chart for standardization
    """
    st.header("Stool Analysis")
    
    stool_data = {}
    
    # 1. Date and Time
    st.subheader("When")
    col1, col2 = st.columns(2)
    with col1:
        stool_data['date'] = st.date_input("Date of bowel movement")
    with col2:
        stool_data['time'] = st.time_input("Time")
    
    # 2. Bristol Stool Chart (7 types)
    st.subheader("Stool Consistency (Bristol Stool Chart)")
    
    bristol_options = {
        "Type 1": "Separate hard lumps, like nuts (Constipation)",
        "Type 2": "Sausage-shaped but lumpy",
        "Type 3": "Sausage-shaped, slightly cracked surface",
        "Type 4": "Smooth and soft, snake-like (Ideal)",
        "Type 5": "Soft blobs with clear-cut edges (Slight diarrhea)",
        "Type 6": "Fluffy pieces with ragged edges (Diarrhea)",
        "Type 7": "Watery, no solid pieces (Severe diarrhea)"
    }
    
    selected_bristol = st.radio(
        "Select stool type",
        options=list(bristol_options.keys()),
        format_func=lambda x: f"{x} - {bristol_options[x]}"
    )
    stool_data['bristol_type'] = selected_bristol
    
    # 3. Color
    st.subheader("Stool Color")
    stool_data['color'] = st.selectbox(
        "Stool Color",
        [
            "Brown (Normal)",
            "Light/Pale",
            "Dark/Black",
            "Red/Reddish",
            "Yellow/Greenish",
            "Gray/White",
            "Orange"
        ]
    )
    
    # 4. Frequency
    st.subheader("Frequency")
    stool_data['frequency'] = st.selectbox(
        "How often per day?",
        ["1", "2", "3", "4", "5+"]
    )
    
    # 5. Abnormal Features
    st.subheader("Abnormal Features (Check if present)")
    abnormal_features = {
        "Blood": st.checkbox("Blood"),
        "Mucus": st.checkbox("Mucus/Slime"),
        "Greasy/Oily": st.checkbox("Greasy/Oily appearance"),
        "Undigested Food": st.checkbox("Undigested Food Particles"),
        "Floating": st.checkbox("Floating (doesn't sink)"),
        "Foul Smelling": st.checkbox("Foul smelling"),
    }
    stool_data['abnormal_features'] = [k for k, v in abnormal_features.items() if v]
    
    # 6. Blood Details (if present)
    if abnormal_features['Blood']:
        st.subheader("Blood Details")
        stool_data['blood_type'] = st.selectbox(
            "Type of blood",
            ["Bright Red", "Dark Red", "Mixed in stool", "On tissue"]
        )
        stool_data['blood_amount'] = st.selectbox(
            "Amount",
            ["Trace/Minimal", "Small", "Moderate", "Significant"]
        )
    
    # 7. Associated Symptoms
    st.subheader("Associated Symptoms")
    symptoms = {
        "Urgency": st.checkbox("Urgency (need to go immediately)"),
        "Straining": st.checkbox("Straining"),
        "Incomplete": st.checkbox("Feeling of incomplete evacuation"),
        "Pain": st.checkbox("Pain/Cramping during bowel movement"),
        "Tenesmus": st.checkbox("Tenesmus (persistent urge after bowel movement)")
    }
    stool_data['symptoms'] = [k for k, v in symptoms.items() if v]
    
    # 8. Medications
    st.subheader("Medications/Factors Affecting Stool")
    stool_data['on_medication'] = st.checkbox("Taking medication that affects digestion?")
    if stool_data['on_medication']:
        stool_data['medication_name'] = st.text_input("Medication name (optional)")
    
    stool_data['recent_antibiotics'] = st.checkbox("Recent antibiotics?")
    
    # 9. Notes
    st.subheader("Additional Notes")
    stool_data['notes'] = st.text_area("Any additional observations")
    
    # 10. Submit Button
    if st.button("Record Stool Analysis"):
        return stool_data
    
    return None


stool_form()