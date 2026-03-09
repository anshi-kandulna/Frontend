# routes/symptom_routes.py
"""
FastAPI routes for handling symptom data
Receives data from frontend and saves to MongoDB
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Initialize MongoDB
MONGO_URI = os.getenv("MONGO_URI")
print(f"🔍 Attempting to connect to MongoDB with URI: {MONGO_URI}")

# Debug: Check if URI is loaded
if not MONGO_URI:
    print("ERROR: MONGO_URI not set in .env file!")
else:
    print(f"✓ MongoDB URI loaded (database: patient)")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ping')
    print("✓ Connected to MongoDB Atlas")
except Exception as e:
    print(f"✗ MongoDB connection error: {e}")

db = client['patient']  # Database name
symptoms_collection = db['patient_symptoms']

# Create FastAPI Router
symptom_router = APIRouter(prefix="/api/symptoms", tags=["symptoms"])

# Request models
class SymptomRequest(BaseModel):
    patient_id: str
    symptoms: List[str]
    severity: Optional[Dict[str, int]] = None
    onset_date: Optional[str] = None
    frequency: Optional[str] = None
    time_of_day: Optional[str] = None
    triggers: Optional[List[str]] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None

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
        print("\n" + "="*50)
        print("📝 SYMPTOM REQUEST RECEIVED")
        print("="*50)
        
        # Validate required fields
        if not data.patient_id:
            raise HTTPException(status_code=400, detail="patient_id required")
        
        # Convert to dict and add timestamps
        symptom_data = data.dict(exclude_none=True)
        symptom_data['created_at'] = datetime.now()
        symptom_data['updated_at'] = datetime.now()
        
        print(f"✓ Patient ID: {data.patient_id}")
        print(f"✓ Symptoms: {data.symptoms}")
        print(f"✓ Data to insert: {symptom_data}")
        print(f"✓ Database: patient")
        print(f"✓ Collection: patient_symptoms")
        
        # Save to MongoDB
        result = symptoms_collection.insert_one(symptom_data)
        
        print(f"✓ INSERT SUCCESSFUL!")
        print(f"✓ Document ID: {result.inserted_id}")
        
        # Verify it was actually saved by reading it back
        verify = symptoms_collection.find_one({"_id": result.inserted_id})
        if verify:
            print(f"✓ VERIFIED: Data found in MongoDB!")
        else:
            print(f"⚠️ WARNING: Data inserted but not found on read-back!")
        
        print("="*50 + "\n")
        
        return {
            "success": True,
            "message": "Symptom record created",
            "id": str(result.inserted_id)
        }
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("="*50 + "\n")
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
