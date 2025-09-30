from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from enum import Enum

class AttractionType(str, Enum):
    RESTAURANT = "restaurant"
    MUSEUM = "museum"
    PARK = "park"
    LANDMARK = "landmark"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    TRANSPORTATION = "transportation"
    HOTEL = "hotel"

class Location(BaseModel):
    lat: float
    lng: float
    address: Optional[str] = None

class Attraction(BaseModel):
    id: str
    name: str
    type: AttractionType
    location: Location
    description: Optional[str] = None
    duration_minutes: int = 60
    cost_usd: float = 0.0
    rating: Optional[float] = None
    images: List[str] = []
    tags: List[str] = []
    opening_hours: Optional[Dict[str, str]] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    google_maps_url: Optional[str] = None

class TimeSlot(BaseModel):
    start_time: time
    end_time: time
    attraction: Attraction
    travel_time_minutes: int = 0  # Time to get to this attraction
    notes: Optional[str] = None

class DayItinerary(BaseModel):
    day_number: int
    date: datetime
    time_slots: List[TimeSlot]
    total_cost: float = 0.0
    total_duration_minutes: int = 0
    color_code: str = "#3B82F6"  # Default blue

class TripPlan(BaseModel):
    id: str
    destination: str
    start_date: datetime
    end_date: datetime
    days: List[DayItinerary]
    total_cost: float = 0.0
    notes: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    text: str
    trip_plan: Optional[TripPlan] = None
    session_id: str
    timestamp: datetime
    suggestions: List[str] = []
    

class OptimizationRequest(BaseModel):
    session_id: str
    action: str  # "reorder", "remove", "discover"
    data: Dict[str, Any]
