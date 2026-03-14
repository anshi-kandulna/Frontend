# services/stool_service.py
"""
Service to handle stool data operations
Connects the frontend form to the backend API
"""

import os

from dotenv import load_dotenv
import requests
from typing import Dict, Optional
from datetime import datetime

load_dotenv()  

class StoolService:
    """Handle stool data submission and retrieval"""
    
    BASE_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api")
    
    #receive stool data from frontend form and send to routes/stool_routes.py
    #static method dont have self. so have to use class name to call other static method
    @staticmethod
    def submit_stool_data(patient_id: str, stool_data: Dict) -> Dict:
        """
        Submit stool data from frontend form to backend
        
        Args:
            patient_id: ID of the patient
            stool_data: Dict from stool_form() containing:
                - date: str
                - bristol_type: str
                - color: str
                - frequency: str
                - abnormal_features: List[str]
                - blood_type: str
                - blood_amount: str
                - symptoms: List[str]
                - on_medication: bool
                - medication_name: str
                - recent_antibiotics: bool
        
        Returns:
            Response from backend with success/error message
        """

        # stool_data["date"]	Error if key missing
        # stool_data.get("date")	Returns None if missing
        try:
            payload = {
                "patient_id": patient_id,
                "date": str(stool_data.get('date')),
                "bristol_type": stool_data.get('bristol_type'),
                "color": stool_data.get('color'),
                "frequency": stool_data.get('frequency'),
                "abnormal_features": stool_data.get('abnormal_features', []),
                "blood_type": stool_data.get('blood_type'),
                "blood_amount": stool_data.get('blood_amount'),
                "symptoms": stool_data.get('symptoms', []),
                "on_medication": stool_data.get('on_medication'),
                "medication_name": stool_data.get('medication_name') if stool_data.get('on_medication') and stool_data.get('medication_name') != '' else None,
                "recent_antibiotics": stool_data.get('recent_antibiotics'),
                "created_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{StoolService.BASE_URL}/stool",
                json=payload,
                timeout=5
            )
            return response.json()
        
        except Exception as e:
            return {"error": str(e), "success": False}