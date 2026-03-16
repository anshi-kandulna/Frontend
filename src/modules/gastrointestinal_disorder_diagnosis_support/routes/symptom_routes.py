# routes/symptom_routes.py
"""
FastAPI routes for handling symptom data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from ..database.mongo import db
from ..models.symptom_model import SymptomRequest, SymptomResponse
#from models.symptom_schema import SYMPTOM_COLLECTION



# Initialize MongoDB
symptoms_collection = db['patient_symptoms']

# Create FastAPI Router
symptom_router = APIRouter(prefix="/api/symptoms", tags=["symptoms"])


@symptom_router.post("", response_model=SymptomResponse)
def create_symptom(data: SymptomRequest):
    """
    Receive symptom data from frontend and save to MongoDB
    """
    try:
        # Validate required fields
        if not data.patient_id:
            raise HTTPException(status_code=400, detail="patient_id required")
        
        # Convert to dict and add timestamps
        symptom_data = data.dict(exclude_none=True)
        
        # Save to MongoDB
        result = symptoms_collection.insert_one(symptom_data)
        
        print(f"✓ INSERT SUCCESSFUL!")
        print(f"✓ Document ID: {result.inserted_id}")
        
        return {
            "success": True,
            "message": "Symptom record created",
            "id": str(result.inserted_id)
        }
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

