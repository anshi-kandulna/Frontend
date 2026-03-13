# components/symptom_form.py

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def symptom_form():
    """
    Collect GI symptom data
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
    
    symptom_data['symptoms'] = selected_symptoms
    
    # 2. Severity Rating (for each symptom)
    if selected_symptoms:
        st.subheader("Severity Rating *")
        for symptom in selected_symptoms:
            severity = st.slider(
                f"{symptom} Severity (1-10)",
                1, 10, 5
            )
            symptom_data[f"{symptom}_severity"] = severity
    
    # 3. Onset Date
    st.subheader("Onset Date *")
    symptom_data['onset_date'] = st.date_input(
        "When did symptoms start?",
        value=None
    )
    
    # 4. Frequency
    st.subheader("Frequency *")
    symptom_data['frequency'] = st.selectbox(
        "How often do you experience this?",
        ["Occasional", "Frequent", "Constant"]
    )
    
    # 5. Time of Day
    st.subheader("Time of Day *")
    symptom_data['time_of_day'] = st.selectbox(
        "When does it usually occur?",
        ["Morning", "Afternoon", "Evening", "Night", "Any time"]
    )
    
    # 6. Triggering Factors
    st.subheader("Potential Triggers *")
    triggers = st.multiselect(
        "What might trigger this?",
        ["Spicy Food", "Dairy", "Stress", "Fatty Food", "Alcohol", "Caffeine", "Unknown"]
    )
    symptom_data['triggers'] = triggers
    
    # 7. Additional Notes
    symptom_data['notes'] = st.text_area("Additional Notes")
    
    # 8. Submit Button
    if st.button("Record Symptoms"):
        # Validate all required fields
        errors = []
        
        if not selected_symptoms:
            errors.append("❌ Please select at least one symptom")
        
        if symptom_data.get('onset_date') is None:
            errors.append("❌ Please select an onset date")
        
        if not triggers:
            errors.append("❌ Please select at least one trigger")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            from services.symptom_service import SymptomService
            
            patient_id = st.session_state.get("patient_id", "patient_001")
            response = SymptomService.submit_symptoms(patient_id, symptom_data)
            
            if response.get('success'):
                st.success(f"✓ Symptoms recorded! ID: {response.get('id')}")
            else:
                st.error(f"Error: {response.get('error', 'Unknown error')}")

symptom_form()