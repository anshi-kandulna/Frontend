import streamlit as st
from ..database import db
import pandas as pd


def stool_analysis_component():

    st.markdown("### Stool Characteristic Analysis")
    patient_id = st.text_input("Enter Patient ID", value="001", key="stool_patient")

    st.markdown("#### Bristol Type Distribution")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SQL Query**")
        st.code(f"""
SELECT 
    bristol_type,
    COUNT(*) AS count
FROM patient_stool
WHERE patient_id = '{patient_id}'
GROUP BY bristol_type
ORDER BY bristol_type ASC;
        """, language="sql")

    with col2:
        st.markdown("**MongoDB Aggregation**")
        st.code(f"""
db.patient_stool.aggregate([
  {{ $match: {{ patient_id: "{patient_id}" }} }},
  {{
    $group: {{
      _id: "$bristol_type",
      count: {{ $sum: 1 }}
    }}
  }},
  {{ $sort: {{ _id: 1 }} }}
])
        """, language="javascript")

    if st.button("▶ Run Bristol Analysis", key="btn_bristol"):
        pipeline = [
            {"$match": {"patient_id": patient_id}},
            {"$group": {"_id": "$bristol_type", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        result = list(db.patient_stool.aggregate(pipeline))
        if result:
            df = pd.DataFrame([
                {"Bristol Type": r["_id"], "Count": r["count"]}
                for r in result
            ])
            st.success("Query executed successfully!")
            st.dataframe(df, use_container_width=True)
            st.markdown("#### Bristol Type Distribution Chart")
            st.bar_chart(df.set_index("Bristol Type")["Count"])
        else:
            st.warning("No stool records found for this patient.")