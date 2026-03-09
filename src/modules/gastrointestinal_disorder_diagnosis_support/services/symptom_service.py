# services/symptom_service.py
"""
Service to handle symptom data operations
Connects the frontend form to the backend API
"""

import os

from dotenv import load_dotenv
import requests
from typing import Dict, Optional
from datetime import datetime

load_dotenv()  

class SymptomService:
    """Handle symptom data submission and retrieval"""
    
    BASE_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api")
    
    @staticmethod
    def submit_symptoms(patient_id: str, symptom_data: Dict) -> Dict:
        """
        Submit symptom data from frontend form to backend
        
        Args:
            patient_id: ID of the patient
            symptom_data: Dict from symptom_form() containing:
                - symptoms: List[str]
                - {symptom}_severity: int for each symptom
                - onset_date: date
                - frequency: str
                - time_of_day: str
                - triggers: List[str]
                - notes: str
        
        Returns:
            Response from backend with success/error message
        """
        try:
            payload = {
                "patient_id": patient_id,
                "symptoms": symptom_data.get('symptoms', []),
                "severity": SymptomService._extract_severities(symptom_data),
                "onset_date": str(symptom_data.get('onset_date')),
                "frequency": symptom_data.get('frequency'),
                "time_of_day": symptom_data.get('time_of_day'),
                "triggers": symptom_data.get('triggers', []),
                "notes": symptom_data.get('notes', ''),
                "created_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{SymptomService.BASE_URL}/symptoms",
                json=payload,
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    @staticmethod
    def _extract_severities(symptom_data: Dict) -> Dict:
        """Extract severity ratings for each symptom"""
        severities = {}
        for key, value in symptom_data.items():
            if "_severity" in key:
                symptom_name = key.replace("_severity", "")
                severities[symptom_name] = value
        return severities
    
    @staticmethod
    def get_patient_symptoms(patient_id: str) -> Dict:
        """
        Retrieve all symptoms for a patient from backend
        
        Args:
            patient_id: ID of the patient
            
        Returns:
            List of symptom records from MongoDB
        """
        try:
            response = requests.get(
                f"{SymptomService.BASE_URL}/symptoms/{patient_id}",
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    @staticmethod
    def get_latest_symptoms(patient_id: str) -> Optional[Dict]:
        """Get the most recent symptom record for a patient"""
        try:
            response = requests.get(
                f"{SymptomService.BASE_URL}/symptoms/{patient_id}/latest",
                timeout=5
            )
            data = response.json()
            return data.get('data') if data.get('success') else None
        except Exception as e:
            return None
