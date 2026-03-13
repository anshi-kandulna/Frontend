# routes/stool_routes.py
"""
FastAPI routes for handling stool data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import os
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client['patient']  # Database name
stool_collection = db['patient_stool']  # Collection name

# Create FastAPI Router
stool_router = APIRouter(prefix="/api/stool", tags=["stool"])

# Request models
class StoolRequest(BaseModel):
    patient_id: str
    date: str
    bristol_type: str = Field(description="Bristol Stool Chart type")
    color: str = Field(description="Stool color")
    frequency: str = Field(description="Frequency of bowel movements")
    abnormal_features: List[str] = Field(default=[], description="List of abnormal features")
    blood_type: Optional[str] = None
    blood_amount: Optional[str] = None
    symptoms: List[str] = Field(default=[], description="Associated symptoms")
    on_medication: bool = Field(description="Whether the patient is on medication")
    medication_name: Optional[str] = None
    recent_antibiotics: bool = Field(description="Whether the patient has taken antibiotics recently")
    notes: Optional[str] = None
    created_at: Optional[str] = None

class StoolResponse(BaseModel):
    success: bool
    message: str
    id: Optional[str] = None

@stool_router.post("", response_model=StoolResponse)
def create_stool(data: StoolRequest):
    """
    Receive stool data from frontend and save to MongoDB
    """
    try:
        # Validate required fields
        if not data.patient_id:
            raise HTTPException(status_code=400, detail="patient_id required")
        
        # Convert to dict and add timestamps
        stool_data = data.dict(exclude_none=True)
        stool_data['created_at'] = datetime.now()
        stool_data['updated_at'] = datetime.now()
        
        
        # Save to MongoDB
        result = stool_collection.insert_one(stool_data)
        
        print(f"✓ INSERT SUCCESSFUL!")
        print(f"✓ Document ID: {result.inserted_id}")
        
        return {
            "success": True,
            "message": "Stool record created",
            "id": str(result.inserted_id)
        }
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))