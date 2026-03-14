# services/diet_service.py
"""
Service to handle diet data operations
Connects the frontend form to the backend API
"""

import os

from dotenv import load_dotenv
import requests
from typing import Dict, Optional
from datetime import datetime

load_dotenv()  

class DietService:
    """Handle diet data submission and retrieval"""
    
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