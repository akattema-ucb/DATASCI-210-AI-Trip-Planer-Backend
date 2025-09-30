from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta, time
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
import uuid
import os
from dotenv import load_dotenv

from models import TripPlan, DayItinerary, TimeSlot, Attraction, Location, AttractionType

load_dotenv()

class TripPlannerAgent:
    """
    Specialized agent for creating detailed trip plans
    Uses LangChain tools to search for attractions, optimize routes, etc.
    """
    
    def __init__(self):
        self.model = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.5,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # TODO: Initialize LangChain tools for:
        # - Google Places API search
        # - Route optimization
        # - Weather checking
        # - Cost estimation
        
    async def plan_trip(
        self,
        user_input: str,
        preferences: Dict[str, Any],
        current_trip: Optional[TripPlan] = None
    ) -> TripPlan:
        """
        Generate a complete trip plan based on user preferences
        """
        # TODO: Implement actual trip planning logic with LangChain
        # This is a placeholder with mock San Francisco data
        
        destination = preferences.get("destination", "San Francisco")
        duration_days = preferences.get("duration_days", 3)
        
        # Mock San Francisco attractions
        sf_attractions = self._get_mock_sf_attractions()
        
        # Create trip plan
        trip_id = str(uuid.uuid4())
        start_date = datetime.now() + timedelta(days=7)  # Start in a week
        
        days = []
        day_colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
        
        for day_num in range(duration_days):
            current_date = start_date + timedelta(days=day_num)
            
            # Create time slots for the day
            time_slots = []
            current_time = time(9, 0)  # Start at 9 AM
            
            # Add 3-4 attractions per day
            day_attractions = sf_attractions[day_num*4:(day_num+1)*4]
            
            for i, attraction in enumerate(day_attractions):
                # Calculate end time based on duration
                start_datetime = datetime.combine(current_date, current_time)
                end_datetime = start_datetime + timedelta(minutes=attraction.duration_minutes)
                
                time_slot = TimeSlot(
                    start_time=current_time,
                    end_time=end_datetime.time(),
                    attraction=attraction,
                    travel_time_minutes=15 if i > 0 else 0,  # 15 min travel between attractions
                    notes=f"Don't miss the {attraction.name}!"
                )
                time_slots.append(time_slot)
                
                # Update current time for next slot
                current_time = (end_datetime + timedelta(minutes=15)).time()
            
            # Create day itinerary
            day_itinerary = DayItinerary(
                day_number=day_num + 1,
                date=current_date,
                time_slots=time_slots,
                total_cost=sum(ts.attraction.cost_usd for ts in time_slots),
                total_duration_minutes=sum(ts.attraction.duration_minutes + ts.travel_time_minutes for ts in time_slots),
                color_code=day_colors[day_num % len(day_colors)]
            )
            days.append(day_itinerary)
        
        # Create complete trip plan
        trip_plan = TripPlan(
            id=trip_id,
            destination=destination,
            start_date=start_date,
            end_date=start_date + timedelta(days=duration_days-1),
            days=days,
            total_cost=sum(day.total_cost for day in days),
            notes="Your personalized San Francisco adventure awaits!"
        )
        
        return trip_plan
    
    def _get_mock_sf_attractions(self) -> List[Attraction]:
        """
        Return mock San Francisco attractions for demo
        """
        return [
            # Day 1 - Classic SF
            Attraction(
                id="1",
                name="Golden Gate Bridge",
                type=AttractionType.LANDMARK,
                location=Location(lat=37.8199, lng=-122.4783, address="Golden Gate Bridge, San Francisco, CA"),
                description="Iconic suspension bridge with stunning views",
                duration_minutes=90,
                cost_usd=0,
                rating=4.8,
                tags=["iconic", "photo-spot", "free"],
                google_maps_url="https://maps.google.com/?q=Golden+Gate+Bridge"
            ),
            Attraction(
                id="2",
                name="Fisherman's Wharf",
                type=AttractionType.ENTERTAINMENT,
                location=Location(lat=37.8080, lng=-122.4177, address="Fisherman's Wharf, San Francisco, CA"),
                description="Bustling waterfront with sea lions, shops, and restaurants",
                duration_minutes=120,
                cost_usd=0,
                rating=4.2,
                tags=["waterfront", "sea-lions", "shopping"],
                google_maps_url="https://maps.google.com/?q=Fishermans+Wharf+SF"
            ),
            Attraction(
                id="3",
                name="Alcatraz Island",
                type=AttractionType.LANDMARK,
                location=Location(lat=37.8267, lng=-122.4230, address="Alcatraz Island, San Francisco, CA"),
                description="Former federal prison on an island",
                duration_minutes=180,
                cost_usd=41.00,
                rating=4.7,
                tags=["history", "island", "tour"],
                google_maps_url="https://maps.google.com/?q=Alcatraz+Island"
            ),
            Attraction(
                id="4",
                name="Ghirardelli Square",
                type=AttractionType.SHOPPING,
                location=Location(lat=37.8059, lng=-122.4230, address="900 North Point St, San Francisco, CA"),
                description="Historic chocolate factory turned shopping center",
                duration_minutes=60,
                cost_usd=20,
                rating=4.5,
                tags=["chocolate", "shopping", "historic"],
                google_maps_url="https://maps.google.com/?q=Ghirardelli+Square"
            ),
            
            # Day 2 - Culture & Parks
            Attraction(
                id="5",
                name="Golden Gate Park",
                type=AttractionType.PARK,
                location=Location(lat=37.7694, lng=-122.4862, address="Golden Gate Park, San Francisco, CA"),
                description="Large urban park with gardens, museums, and trails",
                duration_minutes=180,
                cost_usd=0,
                rating=4.7,
                tags=["nature", "park", "free"],
                google_maps_url="https://maps.google.com/?q=Golden+Gate+Park"
            ),
            Attraction(
                id="6",
                name="California Academy of Sciences",
                type=AttractionType.MUSEUM,
                location=Location(lat=37.7699, lng=-122.4661, address="55 Music Concourse Dr, San Francisco, CA"),
                description="Natural history museum with aquarium and planetarium",
                duration_minutes=180,
                cost_usd=39.95,
                rating=4.6,
                tags=["museum", "science", "family-friendly"],
                google_maps_url="https://maps.google.com/?q=California+Academy+of+Sciences"
            ),
            Attraction(
                id="7",
                name="Haight-Ashbury",
                type=AttractionType.LANDMARK,
                location=Location(lat=37.7692, lng=-122.4481, address="Haight-Ashbury, San Francisco, CA"),
                description="Historic neighborhood, birthplace of 1960s counterculture",
                duration_minutes=90,
                cost_usd=0,
                rating=4.3,
                tags=["history", "shopping", "culture"],
                google_maps_url="https://maps.google.com/?q=Haight+Ashbury"
            ),
            Attraction(
                id="8",
                name="Painted Ladies",
                type=AttractionType.LANDMARK,
                location=Location(lat=37.7763, lng=-122.4327, address="Steiner St & Hayes St, San Francisco, CA"),
                description="Famous Victorian houses from Full House",
                duration_minutes=30,
                cost_usd=0,
                rating=4.4,
                tags=["architecture", "photo-spot", "free"],
                google_maps_url="https://maps.google.com/?q=Painted+Ladies+SF"
            ),
            
            # Day 3 - Downtown & Chinatown
            Attraction(
                id="9",
                name="Chinatown",
                type=AttractionType.LANDMARK,
                location=Location(lat=37.7941, lng=-122.4078, address="Chinatown, San Francisco, CA"),
                description="Largest Chinatown outside Asia",
                duration_minutes=120,
                cost_usd=30,
                rating=4.4,
                tags=["culture", "food", "shopping"],
                google_maps_url="https://maps.google.com/?q=Chinatown+SF"
            ),
            Attraction(
                id="10",
                name="Union Square",
                type=AttractionType.SHOPPING,
                location=Location(lat=37.7880, lng=-122.4074, address="Union Square, San Francisco, CA"),
                description="Premier shopping district",
                duration_minutes=120,
                cost_usd=0,
                rating=4.3,
                tags=["shopping", "dining", "downtown"],
                google_maps_url="https://maps.google.com/?q=Union+Square+SF"
            ),
            Attraction(
                id="11",
                name="Ferry Building Marketplace",
                type=AttractionType.SHOPPING,
                location=Location(lat=37.7955, lng=-122.3937, address="1 Ferry Building, San Francisco, CA"),
                description="Gourmet food market with bay views",
                duration_minutes=90,
                cost_usd=40,
                rating=4.6,
                tags=["food", "market", "waterfront"],
                google_maps_url="https://maps.google.com/?q=Ferry+Building+SF"
            ),
            Attraction(
                id="12",
                name="Coit Tower",
                type=AttractionType.LANDMARK,
                location=Location(lat=37.8024, lng=-122.4058, address="1 Telegraph Hill Blvd, San Francisco, CA"),
                description="Art deco tower with panoramic city views",
                duration_minutes=60,
                cost_usd=10,
                rating=4.5,
                tags=["views", "art-deco", "historic"],
                google_maps_url="https://maps.google.com/?q=Coit+Tower"
            )
        ]
