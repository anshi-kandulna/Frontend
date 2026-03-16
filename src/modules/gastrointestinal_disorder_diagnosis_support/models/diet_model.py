from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

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