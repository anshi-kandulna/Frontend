# routes/diet_routes.py
"""
FastAPI routes for handling diet data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database.mongo import db
from models.diet_model import DietRequest, DietResponse



# Initialize MongoDB
diet_collection = db['patient_diet']  # Collection name

# Create FastAPI Router
diet_router = APIRouter(prefix="/api/diet", tags=["diet"])


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