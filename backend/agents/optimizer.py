from typing import Dict, Any, List
from models import TripPlan, DayItinerary, TimeSlot, Attraction
import copy

class ItineraryOptimizer:
    """
    Agent responsible for optimizing and modifying existing itineraries
    based on user actions (reorder, remove, discover new places)
    """
    
    def __init__(self):
        # TODO: Initialize optimization models and tools
        pass
    
    async def optimize(
        self,
        trip: TripPlan,
        action: str,
        action_data: Dict[str, Any]
    ) -> TripPlan:
        """
        Optimize the itinerary based on the specified action
        """
        # Create a deep copy to avoid modifying the original
        optimized_trip = copy.deepcopy(trip)
        
        if action == "reorder":
            return await self._reorder_attractions(optimized_trip, action_data)
        elif action == "remove":
            return await self._remove_attraction(optimized_trip, action_data)
        elif action == "discover":
            return await self._discover_attractions(optimized_trip, action_data)
        else:
            return optimized_trip
    
    async def _reorder_attractions(
        self,
        trip: TripPlan,
        data: Dict[str, Any]
    ) -> TripPlan:
        """
        Reorder attractions within a day to optimize travel time
        """
        day_number = data.get("day_number")
        new_order = data.get("new_order", [])  # List of attraction IDs in new order
        
        if day_number and 0 < day_number <= len(trip.days):
            day = trip.days[day_number - 1]
            
            # TODO: Implement actual reordering logic
            # For now, just acknowledge the request
            print(f"Reordering day {day_number} with new order: {new_order}")
        
        return trip
    
    async def _remove_attraction(
        self,
        trip: TripPlan,
        data: Dict[str, Any]
    ) -> TripPlan:
        """
        Remove an attraction from the itinerary
        """
        attraction_id = data.get("attraction_id")
        day_number = data.get("day_number")
        
        if day_number and attraction_id and 0 < day_number <= len(trip.days):
            day = trip.days[day_number - 1]
            
            # Filter out the attraction
            day.time_slots = [
                slot for slot in day.time_slots 
                if slot.attraction.id != attraction_id
            ]
            
            # Recalculate timings
            self._recalculate_day_timings(day)
            
            # Update total cost
            day.total_cost = sum(slot.attraction.cost_usd for slot in day.time_slots)
            trip.total_cost = sum(d.total_cost for d in trip.days)
        
        return trip
    
    async def _discover_attractions(
        self,
        trip: TripPlan,
        data: Dict[str, Any]
    ) -> TripPlan:
        """
        Discover and suggest new attractions based on preferences
        """
        day_number = data.get("day_number")
        attraction_type = data.get("type")
        location = data.get("location")
        
        # TODO: Implement actual discovery logic using Google Places API
        # For now, return the original trip
        print(f"Discovering {attraction_type} attractions near {location}")
        
        return trip
    
    def _recalculate_day_timings(self, day: DayItinerary):
        """
        Recalculate time slots after modifications
        """
        if not day.time_slots:
            return
        
        from datetime import datetime, timedelta
        
        # Start at 9 AM
        current_time = datetime.strptime("09:00", "%H:%M").time()
        
        for i, slot in enumerate(day.time_slots):
            slot.start_time = current_time
            
            # Calculate end time
            duration = timedelta(minutes=slot.attraction.duration_minutes)
            end_datetime = datetime.combine(day.date, current_time) + duration
            slot.end_time = end_datetime.time()
            
            # Add travel time for next slot
            if i < len(day.time_slots) - 1:
                travel_time = timedelta(minutes=15)  # Default 15 min between attractions
                current_time = (end_datetime + travel_time).time()
        
        # Update total duration
        day.total_duration_minutes = sum(
            slot.attraction.duration_minutes + slot.travel_time_minutes 
            for slot in day.time_slots
        )
