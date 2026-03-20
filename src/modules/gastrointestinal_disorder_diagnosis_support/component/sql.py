import streamlit as st
from .stoolquery import stool_analysis_component
from .rome import rome_criteria_component
from ..database import db
import pandas as pd


def sql_query_component():

    # ── QUERY 1: Diet-Symptom Correlation (per patient) ──
    st.markdown("### Diet-Symptom Correlation Analysis")
    patient_id_diet = st.text_input("Enter Patient ID", value="001", key="diet_patient")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SQL Query**")
        st.code(f"""
SELECT 
    food_category,
    symptoms_after_eating,
    COUNT(*) AS count
FROM patient_diet
WHERE patient_id = '{patient_id_diet}'
GROUP BY food_category, symptoms_after_eating
ORDER BY count DESC
LIMIT 100;
        """, language="sql")

    with col2:
        st.markdown("**MongoDB Aggregation**")
        st.code(f"""
db.patient_diet.aggregate([
  {{ $match: {{ patient_id: "{patient_id_diet}" }} }},
  {{ $unwind: "$food_category" }},
  {{ $unwind: "$symptoms_after_eating" }},
  {{
    $group: {{
      _id: {{
        food: "$food_category",
        symptom: "$symptoms_after_eating"
      }},
      count: {{ $sum: 1 }}
    }}
  }},
  {{ $sort: {{ count: -1 }} }},
  {{ $limit: 100 }}
])
        """, language="javascript")

    if st.button("▶ Execute Correlation Analysis", key="btn_diet"):
        pipeline = [
            {"$match": {"patient_id": patient_id_diet}},
            {"$unwind": "$food_category"},
            {"$unwind": "$symptoms_after_eating"},
            {
                "$group": {
                    "_id": {
                        "food": "$food_category",
                        "symptom": "$symptoms_after_eating"
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 100}
        ]
        result = list(db.patient_diet.aggregate(pipeline))
        if result:
            data = [{"Food": r["_id"]["food"], "Symptom": r["_id"]["symptom"], "Occurrences": r["count"]} for r in result]
            df = pd.DataFrame(data)
            st.success("Query executed successfully!")
            st.dataframe(df, use_container_width=True)
            st.markdown("#### Correlation Visualization")
            st.bar_chart(df.set_index("Food")["Occurrences"])
        else:
            st.warning("No correlation data found for this patient.")

    st.divider()

    # ── QUERY 2: Temporal Pattern Recognition (per patient) ──
    st.markdown("### Temporal Pattern Recognition")
    patient_id_symptoms = st.text_input("Enter Patient ID", value="001", key="symptom_patient")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SQL Query**")
        st.code(f"""
SELECT 
    symptom,
    DATE(onset_date) AS symptom_day,
    COUNT(*) AS frequency
FROM patient_symptoms
WHERE patient_id = '{patient_id_symptoms}'
GROUP BY symptom, DATE(onset_date)
ORDER BY symptom_day DESC
LIMIT 50;
        """, language="sql")

    with col2:
        st.markdown("**MongoDB Aggregation**")
        st.code(f"""
db.patient_symptoms.aggregate([
  {{ $match: {{ patient_id: "{patient_id_symptoms}" }} }},
  {{ $unwind: "$symptoms" }},
  {{
    $group: {{
      _id: {{
        symptom: "$symptoms.symptom_name",
        day: {{
          $dateToString: {{
            format: "%Y-%m-%d",
            date: "$onset_date"
          }}
        }}
      }},
      frequency: {{ $sum: 1 }}
    }}
  }},
  {{ $sort: {{ "_id.day": -1 }} }},
  {{ $limit: 50 }}
])
        """, language="javascript")

    if st.button("▶ Execute Temporal Pattern Analysis", key="btn_temporal"):
        pipeline = [
            {"$match": {"patient_id": patient_id_symptoms}},
            {"$unwind": "$symptoms"},
            {
                "$group": {
                    "_id": {
                        "symptom": "$symptoms.symptom_name",
                        "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$onset_date"}}
                    },
                    "frequency": {"$sum": 1}
                }
            },
            {"$sort": {"_id.day": -1}},
            {"$limit": 50}
        ]
        result = list(db.patient_symptoms.aggregate(pipeline))
        if result:
            data = [{"Symptom": r["_id"]["symptom"], "Date": r["_id"]["day"], "Frequency": r["frequency"]} for r in result]
            df = pd.DataFrame(data)
            st.success("Query executed successfully!")
            st.dataframe(df, use_container_width=True)
            st.markdown("#### Temporal Pattern Visualization")
            st.line_chart(df.set_index("Date")["Frequency"])
        else:
            st.warning("No temporal patterns found for this patient.")

    st.divider()
    stool_analysis_component()
    st.divider()
    rome_criteria_component()