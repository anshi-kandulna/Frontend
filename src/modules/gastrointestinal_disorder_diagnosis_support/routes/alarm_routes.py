# routes/alarm_routes.py
"""
FastAPI routes for handling alarm data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database.mongo import db
from models.alarm_model import AlarmRequest, AlarmResponse


# Initialize MongoDB
alarm_collection = db['patient_alarms']  

# Create FastAPI Router
alarm_router = APIRouter(prefix="/api/alarms", tags=["alarms"])


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