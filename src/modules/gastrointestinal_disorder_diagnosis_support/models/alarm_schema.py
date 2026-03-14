# models/alarm_schema.py
"""
MongoDB Schema for Alarm Data
Matches the frontend alarm_form.py structure
"""

from datetime import datetime
from typing import List, Optional

class AlarmSchema:
    """
    MongoDB Document Schema for Patient Alarm Data
    
    Collection: patient_alarms
    """
    
    @staticmethod
    def schema():
        return {
            "_id": "ObjectId",  # Auto-generated MongoDB ID
            "patient_id": "ObjectId",  # Link to patient
            "severe_dehydration": "bool",  # Is the patient experiencing severe dehydration?
            "signs_of_dehydration": "List[string]",  # List of dehydration signs
            "weight_loss": "bool",  # Has the patient experienced unexplained weight loss?
            "weight_lost_kg": "float",  # Weight lost in kg
            "weight_loss_period": "string",  # Period over which weight was lost
            "bleeding": "bool",  # Is there blood in the stool?
            "bleeding_type": "string",  # Type of bleeding
            "bleeding_frequency": "string",  # How often the bleeding occurs
            "nocturnal_symptoms": "bool",  # Are there nocturnal symptoms?
            "nocturnal_symptom": "string",  # Which nocturnal symptom?
            "nocturnal_frequency": "string",  # How often per night?
            "family_history": "List[string]",  # Family history of GI conditions
            "fever": "bool",  # Is the patient experiencing fever?
            "fever_temp": "float",  # Temperature in degrees Celsius
            "created_at": "datetime",  # Timestamp when record created
            #"updated_at": "datetime"  # Timestamp when record updated
        }