import streamlit as st
from datetime import datetime
import time
from ..database import db

def trigger_sql_query():
    st.markdown("### Alarm Feature Detection Trigger")
    
    # ── SECTION 1: Side by side SQL vs Atlas ──
    st.subheader("📋 SQL vs MongoDB Atlas Trigger")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**SQL Trigger**")
        st.code("""
CREATE TRIGGER alarm_feature_trigger
AFTER INSERT ON patient_alarms
FOR EACH ROW
BEGIN
    IF NEW.weight_loss = TRUE
    OR NEW.bleeding = TRUE
    OR NEW.nocturnal_symptoms = TRUE
    OR NEW.severe_dehydration = TRUE
    OR NEW.fever = TRUE
    OR NEW.family_history IS NOT NULL
    THEN
        INSERT INTO patient_alarm_alerts (
            patient_id,
            triggered_features,
            alert_message,
            created_at
        )
        VALUES (
            NEW.patient_id,
            NEW.triggered_features,
            'Serious GI alarm feature detected',
            NOW()
        );
    END IF;
END;
        """, language="sql")

    with col2:
        st.markdown("**MongoDB Atlas Trigger**")
        st.code("""
exports = function(changeEvent) {
  var doc = changeEvent["fullDocument"];
  var db = context.services
    .get("mongodb-atlas")
    .db("patient");
  var alerts = db
    .collection("patient_alarm_alerts");
  var fields = [
    "weight_loss", "bleeding",
    "nocturnal_symptoms",
    "severe_dehydration", "fever"
  ];
  var fired = fields.filter(function(f){
    return doc[f] === true;
  });
  var fh = doc.family_history &&
           doc.family_history.length > 0;
  if(fired.length === 0 && !fh) return;
  if(fh){ fired.push("family_history"); }
  alerts.insertOne({
    patient_id:         doc.patient_id,
    triggered_features: fired,
    family_history:     doc.family_history || [],
    alert_message:
      "Serious GI alarm feature detected",
    created_at: new Date()
  });
};
        """, language="javascript")

    st.divider()

    # ── SECTION 2: Live proof form ──
    st.subheader("🧪 Live Trigger Proof")

    with st.form("trigger_proof_form"):
        patient_id = st.text_input("Patient ID", value="proof001")
        col1, col2 = st.columns(2)
        with col1:
            bleeding           = st.checkbox("Bleeding")
            weight_loss        = st.checkbox("Weight Loss")
            fever              = st.checkbox("Fever")
        with col2:
            nocturnal_symptoms = st.checkbox("Nocturnal Symptoms")
            severe_dehydration = st.checkbox("Severe Dehydration")
        family_history = st.multiselect(
            "Family History",
            ["IBD", "IBS", "Colorectal_Cancer", "Gastric_Cancer", "Celiac", "Polyps"]
        )
        submitted = st.form_submit_button("🚀 Insert & Watch Trigger Fire")

    if submitted:
        doc = {
            "patient_id":          patient_id,
            "bleeding":            bleeding,
            "weight_loss":         weight_loss,
            "fever":               fever,
            "nocturnal_symptoms":  nocturnal_symptoms,
            "severe_dehydration":  severe_dehydration,
            "family_history":      family_history,
            "created_at":          datetime.utcnow()
        }

        # Python ONLY writes to patient_alarms
        db.patient_alarms.insert_one(doc)
        insert_time = doc["created_at"]

        # Poll patient_alarm_alerts — Python never writes here
        with st.spinner("⏳ Waiting for Atlas Trigger to fire..."):
            alert = None
            for i in range(10):
                time.sleep(1)
                alert = db.patient_alarm_alerts.find_one(
                    {"patient_id": patient_id},
                    sort=[("created_at", -1)]
                )
                if alert and alert["created_at"] > insert_time:
                    break
                alert = None

        if alert:
            st.success("✅ Atlas Trigger fired!")

            # Side by side proof
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📥 You inserted into `patient_alarms`**")
                st.caption("← Your Python wrote this")
                st.json({
                    "patient_id":    doc["patient_id"],
                    "bleeding":      doc["bleeding"],
                    "weight_loss":   doc["weight_loss"],
                    "fever":         doc["fever"],
                    "family_history": doc["family_history"],
                    "created_at":    str(doc["created_at"])
                })

            with col2:
                st.markdown("**🚨 Atlas Trigger created in `patient_alarm_alerts`**")
                st.caption("← Python NEVER called insert_one() here")
                st.json({
                    "patient_id":         alert.get("patient_id"),
                    "triggered_features": alert.get("triggered_features"),
                    "family_history":     alert.get("family_history"),
                    "alert_message":      alert.get("alert_message"),
                    "created_at":         str(alert.get("created_at"))
                })
        else:
            st.warning("⚠️ No alarm features selected — trigger correctly skipped. Try checking Bleeding or Family History.")

    st.divider()

    # ── SECTION 3: Live patient_alarm_alerts table ──
    st.subheader("🚨 patient_alarm_alerts — Live View")

    if st.button("🔄 Refresh"):
        st.rerun()

    alerts = list(
        db.patient_alarm_alerts
        .find({}, {"_id": 0})
        .sort("created_at", -1)
        .limit(20)
    )

    if alerts:
        import pandas as pd
        df = pd.DataFrame(alerts)
        if "triggered_features" in df.columns:
            df["triggered_features"] = df["triggered_features"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )
        if "family_history" in df.columns:
            df["family_history"] = df["family_history"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )
        st.dataframe(df.head(3), use_container_width=True)  # ← .head(3)
    else:
        st.info("No alerts yet — submit the form above with an alarm feature checked.")