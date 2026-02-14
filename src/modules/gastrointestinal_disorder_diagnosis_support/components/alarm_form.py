# components/alarm_form.py

import streamlit as st
from datetime import datetime

def alarm_form():
    """
    Detect alarm/red flag symptoms indicating serious GI conditions
    Alarm features: Weight loss, bleeding, nocturnal symptoms, fever
    """
    st.header("Red Flag Symptoms (Alarm Features)")
    st.warning("⚠️ If you have any of these symptoms, please consult a doctor immediately!")
    
    alarm_data = {}
    alarm_flags = []

    # 1. Severe Dehydration
    st.subheader("Severe Dehydration")
    has_dehydration = st.checkbox("Signs of severe dehydration?")
    alarm_data['dehydration'] = has_dehydration
    
    if has_dehydration:
        alarm_flags.append("Severe Dehydration")
        dehydration_signs = st.multiselect(
            "Which signs are you experiencing?",
            [
                "Extreme thirst",
                "Dizziness or lightheadedness",
                "Confusion",
                "Dark urine",
                "Dry mouth and lips",
                "Rapid heartbeat",
                "Fainting"
            ]
        )
        alarm_data['dehydration_signs'] = dehydration_signs
        st.error("⛔ Severe dehydration requires immediate medical attention. Go to ER or call emergency services!")
    
    # 2. Weight Loss
    st.subheader("Weight Loss")
    has_weight_loss = st.checkbox("Experienced unexplained weight loss?")
    alarm_data['weight_loss'] = has_weight_loss
    
    if has_weight_loss:
        alarm_flags.append("Weight Loss")
        col1, col2 = st.columns(2)
        with col1:
            alarm_data['weight_lost_kg'] = st.number_input(
                "Weight lost (kg)",
                min_value=0.5,
                step=0.5
            )
        with col2:
            alarm_data['weight_loss_period'] = st.selectbox(
                "Over how long?",
                ["1 week", "2 weeks", "1 month", "2 months", "3+ months"]
            )
        
        st.error("⛔ Unexplained weight loss is a warning sign. Seek medical advice.")
    
    # 3. Bleeding/Blood in Stool
    st.subheader("Bleeding")
    has_bleeding = st.checkbox("Blood in stool or rectal bleeding?")
    alarm_data['bleeding'] = has_bleeding
    
    if has_bleeding:
        alarm_flags.append("Bleeding")
        col1, col2 = st.columns(2)
        with col1:
            alarm_data['bleeding_type'] = st.selectbox(
                "Type of bleeding",
                ["Bright red", "Dark red", "Mixed in stool", "On tissue after wiping"]
            )
        with col2:
            alarm_data['bleeding_frequency'] = st.selectbox(
                "How often?",
                ["Once", "Occasionally", "Frequent", "Every time"]
            )
        
        st.error("⛔ Rectal bleeding requires medical evaluation.")
    
    # 4. Nocturnal Symptoms
    st.subheader("Nocturnal Symptoms")
    has_nocturnal = st.checkbox("Symptoms waking you at night?")
    alarm_data['nocturnal'] = has_nocturnal
    
    if has_nocturnal:
        alarm_flags.append("Nocturnal Symptoms")
        col1, col2 = st.columns(2)
        with col1:
            alarm_data['nocturnal_symptom'] = st.selectbox(
                "Which symptom?",
                ["Diarrhea", "Abdominal pain", "Nausea", "Urgency"]
            )
        with col2:
            alarm_data['nocturnal_frequency'] = st.selectbox(
                "How often per night?",
                ["Once", "2-3 times", "Multiple times"]
            )
        
        st.error("⛔ Nocturnal symptoms suggest significant condition. Seek medical advice.")
    
    # 5. Family History
    st.subheader("Family History")
    st.write("Do you have family members with these conditions?")
    
    family_conditions = {
        "IBD": st.checkbox("Inflammatory Bowel Disease (Crohn's/Ulcerative Colitis)"),
        "Celiac": st.checkbox("Celiac Disease"),
        "IBS": st.checkbox("Irritable Bowel Syndrome"),
        "Colorectal_Cancer": st.checkbox("Colorectal Cancer"),
        "Gastric_Cancer": st.checkbox("Gastric Cancer"),
        "Polyps": st.checkbox("Polyps")
    }
    
    family_history = [k for k, v in family_conditions.items() if v]
    alarm_data['family_history'] = family_history
    
    if "Colorectal_Cancer" in family_history or "Gastric_Cancer" in family_history:
        alarm_flags.append("Family History of Cancer")
        st.warning("⚠️ Family history of cancer increases risk. Regular screening recommended.")
    
    if "IBD" in family_history or "Celiac" in family_history:
        alarm_flags.append("Family History of Serious GI Disease")
        st.info("ℹ️ Your family history increases risk. Monitor symptoms closely.")
    
    # 6. Fever
    st.subheader("Fever")
    has_fever = st.checkbox("Currently have fever (>38°C)?")
    alarm_data['fever'] = has_fever
    
    if has_fever:
        alarm_flags.append("Fever")
        alarm_data['fever_temp'] = st.number_input(
            "Temperature (°C)",
            min_value=38.0,
            step=0.1
        )
        st.error("⛔ Fever with GI symptoms suggests infection. Seek medical care.")
    
    # 7. Summary of Alarms
    st.subheader("Alarm Summary")
    if alarm_flags:
        st.error(f"🚨 **{len(alarm_flags)} Red Flag(s) Detected:**")
        for i, flag in enumerate(alarm_flags, 1):
            st.error(f"  {i}. {flag}")
        st.error("**Please consult a healthcare provider immediately!**")
    else:
        st.success("✅ No red flag symptoms detected. Continue monitoring.")
    
    # 8. Additional Notes
    st.subheader("Additional Information")
    alarm_data['notes'] = st.text_area("Any other concerning symptoms?")
    
    # 9. Submit Button
    if st.button("Record Alarm Assessment"):
        return alarm_data
    
    return None


alarm_form()