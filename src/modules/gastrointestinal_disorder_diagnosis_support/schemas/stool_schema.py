# models/stool_schema.py
"""
MongoDB Schema for Stool Data
Matches the frontend stool_form.py structure
"""

from datetime import datetime
from typing import List, Optional

class StoolSchema:
    """
    MongoDB Document Schema for Patient Stool Data
    
    Collection: patient_stool
    """
    
    @staticmethod
    def schema():
        return {
            "_id": "ObjectId",  # Auto-generated MongoDB ID
            "patient_id": "ObjectId",  # Link to patient
            "date": "date",  # Date of bowel movement
            "bristol_type": "string",  # 'Type 1' to 'Type 7'
            "color": "string",  # Stool color
            "frequency": "string",  # '1' to '5+'
            "abnormal_features": "List[string]",  # ['Blood', 'Mucus', ...]
            "blood_type": "string",  # 'Bright Red', 'Dark Red', etc.
            "blood_amount": "string",  # 'Trace/Minimal', 'Small', etc.
            "symptoms": "List[string]",  # ['Urgency', 'Straining', ...]
            "on_medication": "bool",  # Whether the patient is on medication
            "medication_name": "string",  # Name of the medication (optional)
            "recent_antibiotics": "bool",  # Whether the patient has taken antibiotics recently
            "created_at": "datetime",  # Timestamp when record created
            #"updated_at": "datetime"  # Timestamp when record updated
        }