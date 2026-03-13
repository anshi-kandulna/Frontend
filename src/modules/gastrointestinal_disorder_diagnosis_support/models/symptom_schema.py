# models/symptom_schema.py
"""
MongoDB Schema for Symptom Data
Matches the frontend symptom_form.py structure
"""

from datetime import datetime
from typing import List, Optional

class SymptomSchema:
    """
    MongoDB Document Schema for Patient Symptoms
    
    Collection: patient_symptoms
    """
    
    @staticmethod
    def schema():
        return {
            "_id": "ObjectId",  # Auto-generated MongoDB ID
            "patient_id": "string",  # Link to patient
            "symptoms": "List[string]",  # ['Abdominal Pain', 'Diarrhea', ...]
            "severity": {
                "[symptom_name]": "int (1-10)"  # Where [symptom_name] = any symptom from the 'symptoms' array
            },
            "onset_date": "datetime",  # When symptoms started
            "frequency": "string",  # 'Occasional' | 'Frequent' | 'Constant'
            "time_of_day": "string",  # 'Morning' | 'Afternoon' | 'Evening' | 'Night' | 'Any time'
            "triggers": "List[string]",  # ['Spicy Food', 'Dairy', 'Stress', ...]
            "notes": "string",  # Additional notes
            "created_at": "datetime",  # Timestamp when record created
            "updated_at": "datetime"  # Timestamp when record updated
        }
    
    @staticmethod
    def example_document():
        """Example MongoDB document"""
        return {
            "_id": "ObjectId",
            "patient_id": "patient_001",
            "symptoms": ["Abdominal Pain", "Nausea"],
            "severity": {
                "Abdominal Pain": 7,
                "Nausea": 5
            },
            "onset_date": datetime(2026, 3, 5),
            "frequency": "Frequent",
            "time_of_day": "Morning",
            "triggers": ["Spicy Food", "Stress"],
            "notes": "Pain increases after eating",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }


# MongoDB Collection Creation (run once in backend)
# SYMPTOM_COLLECTION = {
#     "name": "patient_symptoms",
#     "indexes": [
#         {"key": "patient_id", "unique": False},
#         {"key": "created_at", "unique": False},
#         {"key": ["patient_id", "created_at"], "unique": False}
#     ]
# }