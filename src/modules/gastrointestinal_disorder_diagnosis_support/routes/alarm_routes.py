# routes/alarm_routes.py
"""
FastAPI routes for handling alarm data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from pymongo import MongoClient
from bson import ObjectId

from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client['patient']  # Database name
alarm_collection = db['patient_alarms']  # Collection name

# Create FastAPI Router
alarm_router = APIRouter(prefix="/api/alarms", tags=["alarms"])

# Request models
class AlarmRequest(BaseModel):
    patient_id: str
    severe_dehydration: bool = False
    signs_of_dehydration: Optional[List[str]] = []
    weight_loss: bool = False
    weight_lost_kg: Optional[float] = None
    weight_loss_period: Optional[str] = None
    bleeding: bool = False
    bleeding_type: Optional[str] = None
    bleeding_frequency: Optional[str] = None
    nocturnal_symptoms: bool = False
    nocturnal_symptom: Optional[str] = None
    nocturnal_frequency: Optional[str] = None
    family_history: List[str] = []
    fever: bool = False
    fever_temp: Optional[float] = None
    created_at: datetime

class AlarmResponse(BaseModel):
    success: bool
    message: str
    id: Optional[str] = None

@alarm_router.post("", response_model=AlarmResponse)
def create_alarm(data: AlarmRequest):
    """
    Receive alarm data from frontend and save to MongoDB
    """
    try:
        # Validate required fields
        if not data.patient_id:
            raise HTTPException(status_code=400, detail="patient_id required")

        # Convert to dict 
        alarm_data = data.dict(exclude_none=True)

        # Save to MongoDB
        result = alarm_collection.insert_one(alarm_data)

        print(f"✓ INSERT SUCCESSFUL!")
        print(f"✓ Document ID: {result.inserted_id}")

        return {
            "success": True,
            "message": "Alarm record created",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))