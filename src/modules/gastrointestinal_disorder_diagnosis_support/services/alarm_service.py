# services/alarm_service.py
"""
Service to handle alarm data operations
Connects the frontend form to the backend API
"""

import os

from dotenv import load_dotenv
import requests
from typing import Dict, Optional
from datetime import datetime

load_dotenv()  

class AlarmService:
    """Handle alarm data submission and retrieval"""
    
    BASE_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api")
    
    #receive alarm data from frontend form and send to routes/alarm_routes.py
    @staticmethod
    def submit_alarm_data(patient_id: str, alarm_data: Dict) -> Dict:
        """
        Submit alarm data from frontend form to backend
        
        Args:
            patient_id: ID of the patient
            alarm_data: Dict from alarm_form() containing:
                - severe_dehydration: bool
                - signs_of_dehydration: List[str]
                - weight_loss: bool
                - weight_lost_kg: float
                - weight_loss_period: str
                - bleeding: bool
                - bleeding_type: str
                - bleeding_frequency: str
                - nocturnal_symptoms: bool
                - nocturnal_symptom: str
                - nocturnal_frequency: str
                - family_history: List[str]
                - fever: bool
                - fever_temp: float
        
        Returns:
            Response from backend with success/error message
        """

        try:
            payload = {
                "patient_id": patient_id,
                "severe_dehydration": alarm_data.get('severe_dehydration'),
                "signs_of_dehydration": alarm_data.get('signs_of_dehydration', []),
                "weight_loss": alarm_data.get('weight_loss'),
                "weight_lost_kg": alarm_data.get('weight_lost_kg'),
                "weight_loss_period": alarm_data.get('weight_loss_period'),
                "bleeding": alarm_data.get('bleeding'),
                "bleeding_type": alarm_data.get('bleeding_type'),
                "bleeding_frequency": alarm_data.get('bleeding_frequency'),
                "nocturnal_symptoms": alarm_data.get('nocturnal_symptoms'),
                "nocturnal_symptom": alarm_data.get('nocturnal_symptom'),
                "nocturnal_frequency": alarm_data.get('nocturnal_frequency'),
                "family_history": alarm_data.get('family_history', []),
                "fever": alarm_data.get('fever'),
                "fever_temp": alarm_data.get('fever_temp'),
                "created_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{AlarmService.BASE_URL}/alarms",
                json=payload,
                timeout=5
            )
            return response.json()
        
        except Exception as e:
            return {"error": str(e), "success": False}