from pymongo import MongoClient
from database.mongo import db

# Delete all test documents
result = db.patient_alarms.delete_many({"patient_id": "test005"})
print(f"Deleted {result.deleted_count} documents from patient_alarms")

result2 = db.patient_alarm_alerts.delete_many({"patient_id": "test005"})
print(f"Deleted {result2.deleted_count} documents from patient_alarms")