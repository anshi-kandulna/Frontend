from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# Request models
class StoolRequest(BaseModel):
    #model_config = ConfigDict(arbitrary_types_allowed=True)
    #patient_id: ObjectId
    patient_id: str
    date: datetime #pydantic will automatically convert date string to datetime object
    bristol_type: str 
    color: Optional[str] = None
    frequency: str
    abnormal_features: List[str] = []
    symptoms: List[str] = []
    on_medication: bool 
    medication_name: Optional[str] = None
    recent_antibiotics: bool 
    created_at: datetime

class StoolResponse(BaseModel):
    success: bool
    message: str
    id: Optional[str] = None