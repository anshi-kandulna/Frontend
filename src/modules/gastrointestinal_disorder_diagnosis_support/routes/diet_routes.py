# routes/diet_routes.py
"""
FastAPI routes for handling diet data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import os
from pymongo import MongoClient
from bson import ObjectId

from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client['patient']  # Database name
diet_collection = db['patient_diet']  # Collection name

# Create FastAPI Router
diet_router = APIRouter(prefix="/api/diet", tags=["diet"])

# Request models
class DietRequest(BaseModel):
    #model_config = ConfigDict(arbitrary_types_allowed=True)
    #patient_id: ObjectId
    patient_id: str
    meal_time: datetime
    food_category: List[str]
    portion_size: Optional[str] = None
    allergens: List[str] = []
    symptoms_after_eating: List[str] = []
    created_at: datetime

class DietResponse(BaseModel):
    success: bool
    message: str
    id: Optional[str] = None

@diet_router.post("", response_model=DietResponse)
def create_diet(data: DietRequest):
    """
    Receive diet data from frontend and save to MongoDB
    """
    try:
        # Validate required fields
        if not data.patient_id:
            raise HTTPException(status_code=400, detail="patient_id required")

        # Convert to dict 
        diet_data = data.dict(exclude_none=True)

        # Save to MongoDB
        result = diet_collection.insert_one(diet_data)

        print(f"✓ INSERT SUCCESSFUL!")
        print(f"✓ Document ID: {result.inserted_id}")

        return {
            "success": True,
            "message": "Diet record created",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))