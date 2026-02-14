# components/symptom_form.py

import streamlit as st

def symptom_form():
    """
    Collect GI symptom data
    """
    st.header("Symptom Assessment")
    
    symptom_data = {}
    
    # 1. Symptom Selection
    st.subheader("Select Your Symptoms")
    symptoms = [
        "Abdominal Pain",
        "Diarrhea",
        "Nausea",
        "Vomiting"
    ]
    selected_symptoms = []
    for symptom in symptoms:
        if st.checkbox(symptom):
            selected_symptoms.append(symptom)
    
    symptom_data['symptoms'] = selected_symptoms
    
    # 2. Severity Rating (for each symptom)
    if selected_symptoms:
        st.subheader("Severity Rating")
        for symptom in selected_symptoms:
            severity = st.slider(
                f"{symptom} Severity (1-10)",
                1, 10, 5
            )
            symptom_data[f"{symptom}_severity"] = severity
    
    # 3. Onset Date
    st.subheader("Onset Date")
    symptom_data['onset_date'] = st.date_input(
        "When did symptoms start?",
        value=None
    )
    
    # 4. Frequency
    st.subheader("Frequency")
    symptom_data['frequency'] = st.selectbox(
        "How often do you experience this?",
        ["Occasional", "Frequent", "Constant"]
    )
    
    # 5. Time of Day
    symptom_data['time_of_day'] = st.selectbox(
        "When does it usually occur?",
        ["Morning", "Afternoon", "Evening", "Night", "Any time"]
    )
    
    # 6. Triggering Factors
    st.subheader("Potential Triggers")
    triggers = st.multiselect(
        "What might trigger this?",
        ["Spicy Food", "Dairy", "Stress", "Fatty Food", "Alcohol", "Caffeine", "Unknown"]
    )
    symptom_data['triggers'] = triggers
    
    # 7. Additional Notes
    symptom_data['notes'] = st.text_area("Additional Notes")
    
    # 8. Submit Button
    if st.button("Record Symptoms"):
        return symptom_data
    
    return None

symptom_form()