from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class TripRequest(BaseModel):
    origin: str
    destination: str
    preferences: Dict[str, Any] = Field(default_factory=dict)

class TransitRoute(BaseModel):
    mode: str
    duration: str
    cost: Optional[str] = None
    details: str

class TripPlan(BaseModel):
    plan: str
    routes_data: List[TransitRoute]
    total_duration: Optional[str] = None
    total_cost: Optional[str] = None

class TripResponse(BaseModel):
    plan: str
    routes_data: List[TransitRoute]
