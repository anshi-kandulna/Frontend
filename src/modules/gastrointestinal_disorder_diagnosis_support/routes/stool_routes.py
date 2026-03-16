# routes/stool_routes.py
"""
FastAPI routes for handling stool data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from bson import ObjectId
from ..database.mongo import db
from ..models.stool_model import StoolRequest, StoolResponse


# Initialize MongoDB
stool_collection = db['patient_stool']  # Collection name

# Create FastAPI Router
stool_router = APIRouter(prefix="/api/stool", tags=["stool"])


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