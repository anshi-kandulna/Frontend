from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

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