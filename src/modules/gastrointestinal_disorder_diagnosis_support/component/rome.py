import streamlit as st
from ..database import db
import pandas as pd
from datetime import datetime, timedelta


def rome_criteria_component():

    st.markdown("### Rome IV IBS Detection")
    patient_id = st.text_input("Enter Patient ID", value="001", key="rome_patient")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SQL Query**")
        st.code(f"""
-- Check 1: Abdominal pain >= 4 times in last 3 months
SELECT patient_id
FROM patient_symptoms
JOIN symptom_items ON patient_symptoms.id = symptom_items.symptom_record_id
WHERE patient_id = '{patient_id}'
  AND LOWER(symptom_name) = 'abdominal pain'
  AND onset_date >= NOW() - INTERVAL '3 months'
HAVING COUNT(*) >= 4;

-- Check 2: 2+ different bristol types
SELECT patient_id
FROM patient_stool
WHERE patient_id = '{patient_id}'
  AND date >= NOW() - INTERVAL '3 months'
HAVING COUNT(DISTINCT bristol_type) >= 2;

-- Check 3: 2+ different frequencies
SELECT patient_id
FROM patient_stool
WHERE patient_id = '{patient_id}'
  AND date >= NOW() - INTERVAL '3 months'
HAVING COUNT(DISTINCT frequency) >= 2;
        """, language="sql")

    with col2:
        st.markdown("**MongoDB Aggregation**")
        st.code(f"""
-- Check 1: Abdominal pain >= 4 times
db.patient_symptoms.aggregate([
  {{ $match: {{ patient_id: "{patient_id}" }} }},
  {{ $unwind: "$symptoms" }},
  {{ $match: {{
      "symptoms.symptom_name": /abdominal pain/i,
      onset_date: {{ $gte: <3 months ago> }}
  }} }},
  {{ $group: {{ _id: "$patient_id", count: {{ $sum: 1 }} }} }},
  {{ $match: {{ count: {{ $gte: 4 }} }} }}
])

-- Check 2: 2+ distinct bristol types
db.patient_stool.aggregate([
  {{ $match: {{ patient_id: "{patient_id}" }} }},
  {{ $group: {{ _id: "$patient_id",
      types: {{ $addToSet: "$bristol_type" }} }} }},
  {{ $match: {{ "types.1": {{ $exists: true }} }} }}
])

-- Check 3: 2+ distinct frequencies
db.patient_stool.aggregate([
  {{ $match: {{ patient_id: "{patient_id}" }} }},
  {{ $group: {{ _id: "$patient_id",
      freqs: {{ $addToSet: "$frequency" }} }} }},
  {{ $match: {{ "freqs.1": {{ $exists: true }} }} }}
])
        """, language="javascript")

    if st.button("▶ Run Rome IV IBS Detection", key="btn_rome"):

        three_months_ago = datetime.utcnow() - timedelta(days=90)

        # ── Check 1: Abdominal pain >= 4 times in last 3 months ──
        pipeline_pain = [
            {"$match": {"patient_id": patient_id, "onset_date": {"$gte": three_months_ago}}},
            {"$unwind": "$symptoms"},
            {"$match": {"symptoms.symptom_name": {"$regex": "abdominal pain", "$options": "i"}}},
            {"$group": {"_id": "$patient_id", "pain_count": {"$sum": 1}}},
            {"$match": {"pain_count": {"$gte": 4}}}
        ]
        pain_result = list(db.patient_symptoms.aggregate(pipeline_pain))
        pain_met = len(pain_result) > 0
        pain_count = pain_result[0]["pain_count"] if pain_result else 0

        # ── Check 2: 2+ distinct bristol types ──
        pipeline_form = [
            {"$match": {"patient_id": patient_id, "date": {"$gte": three_months_ago}}},
            {"$group": {"_id": "$patient_id", "bristol_types": {"$addToSet": "$bristol_type"}}},
            {"$match": {"bristol_types.1": {"$exists": True}}}
        ]
        form_result = list(db.patient_stool.aggregate(pipeline_form))
        form_met = len(form_result) > 0
        bristol_types = form_result[0]["bristol_types"] if form_result else []

        # ── Check 3: 2+ distinct frequencies ──
        pipeline_freq = [
            {"$match": {"patient_id": patient_id, "date": {"$gte": three_months_ago}}},
            {"$group": {"_id": "$patient_id", "frequencies": {"$addToSet": "$frequency"}}},
            {"$match": {"frequencies.1": {"$exists": True}}}
        ]
        freq_result = list(db.patient_stool.aggregate(pipeline_freq))
        freq_met = len(freq_result) > 0
        frequencies = freq_result[0]["frequencies"] if freq_result else []

        # ── Results table ──
        st.markdown("#### Criteria Checklist")
        df = pd.DataFrame([
            {
                "Criterion": "Abdominal pain >= 4 times in last 3 months",
                "Status": "Met" if pain_met else "Not Met",
                "Detail": f"{pain_count} occurrence(s) found"
            },
            {
                "Criterion": "Change in stool form (2+ bristol types)",
                "Status": "Met" if form_met else "Not Met",
                "Detail": f"Types found: {', '.join(bristol_types) if bristol_types else 'N/A'}"
            },
            {
                "Criterion": "Change in stool frequency (2+ distinct frequencies)",
                "Status": "Met" if freq_met else "Not Met",
                "Detail": f"Frequencies found: {', '.join(frequencies) if frequencies else 'N/A'}"
            }
        ])
        st.dataframe(df, use_container_width=True)

        # ── Final diagnosis ──
        criteria_met = sum([pain_met, form_met, freq_met])
        st.markdown("#### Diagnosis")
        if criteria_met == 3:
            st.error(f"IBS - Rome IV Positive ({criteria_met}/3 criteria met)")
        elif criteria_met == 2:
            st.warning(f"Borderline IBS - Monitor Patient ({criteria_met}/3 criteria met)")
        else:
            st.success(f"IBS Not Confirmed ({criteria_met}/3 criteria met)")