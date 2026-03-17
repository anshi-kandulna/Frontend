import streamlit as st
from ..database import db


def sql_query_component():
    
    # ── QUERY 1: Alarm Feature Trigger ──
    st.markdown("### Diet-Symptom Correlation Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SQL Query**")
        st.code("""
CREATE TRIGGER alarm_feature_trigger
AFTER INSERT ON alarm_requests
FOR EACH ROW
BEGIN
    IF NEW.weight_loss = TRUE
    OR NEW.bleeding = TRUE
    OR NEW.nocturnal_symptoms = TRUE
    OR NEW.severe_dehydration = TRUE
    OR NEW.fever = TRUE
    THEN
        INSERT INTO alarm_alerts (
            patient_id,
            alert_message,
            created_at
        )
        VALUES (
            NEW.patient_id,
            'Serious GI alarm feature detected',
            NOW()
        );
    END IF;
END;
        """, language="sql")

    with col2:
        st.markdown("**MongoDB Aggregation**")
        st.code("""
db.patient_diet.aggregate([
  { $unwind: "$food_category" },
  { $unwind: "$symptoms_after_eating" },
  {
    $group: {
      _id: {
        food: "$food_category",
        symptom: "$symptoms_after_eating"
      },
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } },
  { $limit: 100 }
])
        """, language="javascript")

    if st.button("▶ Execute Correlation Analysis"):
        pipeline = [
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
            import pandas as pd
            data = [{"Food": r["_id"]["food"], "Symptom": r["_id"]["symptom"], "Occurrences": r["count"]} for r in result]
            df = pd.DataFrame(data)
            st.success("Query executed successfully!")
            st.dataframe(df, use_container_width=True)
            st.markdown("#### Correlation Visualization")
            st.bar_chart(df.set_index("Food")["Occurrences"])
        else:
            st.warning("No correlation data found.")

    st.divider()

    # ── QUERY 2: Temporal Pattern Recognition ──
    st.markdown("### Temporal Pattern Recognition")
    patient_id = st.text_input("Enter Patient ID", value="002")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SQL Query**")
        st.code(f"""
SELECT 
    symptom,
    DATE(onset_date) AS symptom_day,
    COUNT(*) AS frequency
FROM patient_symptoms
WHERE patient_id = '{patient_id}'
GROUP BY symptom, DATE(onset_date)
ORDER BY symptom_day DESC
LIMIT 50;
        """, language="sql")

    with col2:
        st.markdown("**MongoDB Aggregation**")
        st.code(f"""
db.patient_symptoms.aggregate([
  {{ $match: {{ patient_id: "{patient_id}" }} }},
  {{
    $group: {{
      _id: {{
        symptom: "$symptom",
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

    if st.button("▶ Execute Temporal Pattern Analysis"):
        pipeline = [
            {"$match": {"patient_id": patient_id}},
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
            import pandas as pd
            data = [{"Symptom": r["_id"]["symptom"], "Date": r["_id"]["day"], "Frequency": r["frequency"]} for r in result]
            df = pd.DataFrame(data)
            st.success("Query executed successfully!")
            st.dataframe(df, use_container_width=True)
            st.markdown("#### Temporal Pattern Visualization")
            st.line_chart(df.set_index("Date")["Frequency"])
        else:
            st.warning("No temporal patterns found.")