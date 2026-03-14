# routes/symptom_routes.py
"""
FastAPI routes for handling symptom data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from datetime import datetime
import os
from pymongo import MongoClient
from bson import ObjectId
#from models.symptom_schema import SYMPTOM_COLLECTION

from dotenv import load_dotenv

load_dotenv()

# Initialize MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client['patient']  # Database name
symptoms_collection = db['patient_symptoms']

# Create FastAPI Router
symptom_router = APIRouter(prefix="/api/symptoms", tags=["symptoms"])

class Symptom(BaseModel):
    symptom_name: str = Field(..., description="Name of the symptom")
    severity_rating: int = Field(..., ge=1, le=10, description="Severity rating 1-10")

# Request models
class SymptomRequest(BaseModel):
    #model_config = ConfigDict(arbitrary_types_allowed=True)
    #patient_id: ObjectId
    patient_id: str
    symptoms: List[Symptom] = Field(min_items=1, description="At least one symptom required")
    onset_date: Optional[datetime] = None
    frequency: Optional[str] = None
    time_of_day: Optional[str] = None
    triggers: List[str] = []
    created_at: datetime

class SymptomResponse(BaseModel):
    success: bool
    message: str
    id: Optional[str] = None

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

@symptom_router.get("/{patient_id}")
def get_symptoms(patient_id: str):
    """
    Get all symptom records for a patient
    """
    try:
        symptoms = list(symptoms_collection.find(
            {"patient_id": patient_id},
            {"_id": 1, "symptoms": 1, "severity": 1, "created_at": 1, "notes": 1}
        ).sort("created_at", -1))  # Newest first
        
        # Convert ObjectId to string
        for symptom in symptoms:
            symptom['_id'] = str(symptom['_id'])
            if 'created_at' in symptom:
                symptom['created_at'] = symptom['created_at'].isoformat()

        print(f"✓ RETRIEVED {len(symptoms)} SYMPTOM RECORD(S) FOR PATIENT ID: {patient_id}")

        return {
            "success": True,
            "data": symptoms
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@symptom_router.get("/{patient_id}/latest")
def get_latest_symptom(patient_id: str):
    """
    Get the most recent symptom record for a patient
    """
    try:
        symptom = symptoms_collection.find_one(
            {"patient_id": patient_id},
            sort=[("created_at", -1)]  # Newest first
        )
        
        if not symptom:
            raise HTTPException(status_code=404, detail="No symptoms found")
        
        # Convert ObjectId to string
        symptom['_id'] = str(symptom['_id'])
        if 'created_at' in symptom:
            symptom['created_at'] = symptom['created_at'].isoformat()
        
        return {
            "success": True,
            "data": symptom
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@symptom_router.delete("/{patient_id}")
def delete_symptom(patient_id: str):
    """
    Delete a symptom record
    """
    try:
        result = symptoms_collection.delete_one({"patient_id": patient_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Record not found")
        
        return {
            "success": True,
            "message": "Symptom record deleted"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
