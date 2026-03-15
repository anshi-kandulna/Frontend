# components/symptom_form.py

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def symptom_form():
    """
    Collect GI symptom data
    Returns: dict with symptom data
    """
    st.header("Symptom Assessment")
    
    symptom_data = {}
    
    # 1. Symptom Selection
    st.subheader("Select Your Symptoms *")  # Asterisk indicates required
    symptoms = [
        "Abdominal Pain",
        "Diarrhea",
        "Nausea",
        "Vomiting"
    ]
    selected_symptoms = []
    for symptom in symptoms:
        if st.checkbox(symptom, key=f"checkbox_{symptom}"):
            selected_symptoms.append(symptom)

    
    # 2. Severity Rating (for each symptom)
    if selected_symptoms:
        symptom_data['symptoms'] = []
        st.subheader("Severity Rating")
        for symptom in selected_symptoms:
            severity = st.slider(
                f"{symptom} Severity (1-10)",
                1, 10, 5
            )
            symptom_data['symptoms'].append({"symptom_name": symptom, "severity_rating": severity})

    # 3. Onset Date
    st.subheader("Onset Date")
    symptom_data['onset_date'] = st.date_input(
        "When did symptoms start?",
        value=None,
        key="onset_date"
    )
    
    # 4. Frequency
    st.subheader("Frequency")
    symptom_data['frequency'] = st.selectbox(
        "How often do you experience this?",
        ["Occasional", "Frequent", "Constant"],
        index=None,
        placeholder="Select frequency"
    )
    
    # 5. Time of Day
    st.subheader("Time of Day")
    symptom_data['time_of_day'] = st.selectbox(
        "When does it usually occur?",
        ["Morning", "Afternoon", "Evening", "Night", "Any time"],
        index=None,
        placeholder="Select a time of day"
    )
    
    # 6. Triggering Factors
    st.subheader("Potential Triggers")
    triggers = st.multiselect(
        "What might trigger this?",
        ["Spicy Food", "Dairy", "Stress", "Fatty Food", "Alcohol", "Caffeine"],
    )
    symptom_data['triggers'] = triggers
    
    return symptom_data

    
#symptom_form()