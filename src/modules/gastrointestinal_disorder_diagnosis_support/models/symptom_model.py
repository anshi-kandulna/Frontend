from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

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