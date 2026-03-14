# models/diet_schema.py
"""
MongoDB Schema for Diet Data
Matches the frontend diet_form.py structure
"""

from datetime import datetime
from typing import List, Optional

class DietSchema:
    """
    MongoDB Document Schema for Patient Diet Data
    
    Collection: patient_diet
    """
    
    @staticmethod
    def schema():
        return {
            "_id": "ObjectId",  # Auto-generated MongoDB ID
            "patient_id": "ObjectId",  # Link to patient
            "date": "date",  # Date of food intake
            "time": "string",  # Time of food intake
            "food_category": "List[string]",  # Category of food consumed
            "portion_size": "string",  # Portion size (e.g., 'Small', 'Medium', 'Large')
            "allergens": "List[string]",  # List of allergens (e.g., 'Milk', 'Gluten', etc.)
            "symptoms_after_eating": "List[string]",  # List of symptoms experienced after eating
            "created_at": "datetime",  # Timestamp when record created
            #"updated_at": "datetime"  # Timestamp when record updated
        }