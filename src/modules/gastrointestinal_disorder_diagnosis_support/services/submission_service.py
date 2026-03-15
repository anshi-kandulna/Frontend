# services/submission_service.py
"""
Service to handle all forms submission
Connects the frontend form to the backend API
"""

import os

from dotenv import load_dotenv
import requests
from typing import Dict, Optional
from datetime import datetime
from .symptom_service import SymptomService
from .stool_service import StoolService
from .diet_service import DietService
from .alarm_service import AlarmService

load_dotenv()  




class SubmissionService:
    """Handle submission of all forms"""
    
    BASE_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api")
    
    #receive diet data from frontend form and send to routes/diet_routes.py
    @staticmethod
    def submit_diet_data(patient_id: str, diet_data: Dict) -> Dict:
        """
        Submit diet data from frontend form to backend
        
        Args:
            patient_id: ID of the patient
            diet_data: Dict from diet_form() containing:
                - date: str
                - time: str
                - food_category: List[str]
                - portion_size: str
                - allergens: List[str]
                - symptoms_after_eating: List[str]
        
        Returns:
            Response from backend with success/error message
        """

        try:
            payload = {
                "patient_id": patient_id,
                "meal_time": diet_data.get('meal_time'),
                "food_category": diet_data.get('food_category'),
                "portion_size": diet_data.get('portion_size') if diet_data.get('portion_size') != "" else None,
                "allergens": diet_data.get('allergens', []),
                "symptoms_after_eating": diet_data.get('symptoms_after_eating', []),
                "created_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{DietService.BASE_URL}/diet",
                json=payload,
                timeout=5
            )
            return response.json()
        
        except Exception as e:
            return {"error": str(e), "success": False}

class FormSubmissionHandler:
    """Handle submission of all forms"""
    
    @staticmethod
    def submit_all_forms(patient_id: str, symptom_data: Dict, stool_data: Dict, diet_data: Dict, alarm_data: Dict) -> Dict:
        """
        Submit all form data to backend
        
        Args:
            patient_id: ID of the patient
            symptom_data: Dict from symptom_form()
            stool_data: Dict from stool_form()
            diet_data: Dict from diet_form()
            alarm_data: Dict from alarm_form()
        
        Returns:
            Combined response from backend for all submissions
        """
        responses = {}
        
        responses['symptoms'] = SymptomService.submit_symptoms(patient_id, symptom_data)
        responses['stool'] = StoolService.submit_stool_data(patient_id, stool_data)
        responses['diet'] = DietService.submit_diet_data(patient_id, diet_data)
        responses['alarm'] = AlarmService.submit_alarm_data(patient_id, alarm_data)
        
        return responses
