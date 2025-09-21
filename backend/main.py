from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import asyncio
from contextlib import asynccontextmanager

from models import ChatRequest, ChatResponse, TripPlan, Attraction, DayItinerary
from agents.trip_planner import TripPlannerAgent
from agents.chat_agent import ChatAgent
from agents.optimizer import ItineraryOptimizer

# Store active connections and trip data in memory
active_connections: List[WebSocket] = []
user_trips: Dict[str, TripPlan] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up AI Travel Planner...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(title="AI Travel Planner API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
chat_agent = ChatAgent()
trip_planner = TripPlannerAgent()
optimizer = ItineraryOptimizer()

@app.get("/")
async def root():
    return {"message": "AI Travel Planner API is running"}

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint that processes user messages and returns both
    conversational responses and trip planning data
    """
    # Get or create user session
    session_id = request.session_id or "default"
    
    # Process message with chat agent
    chat_response = await chat_agent.process_message(
        message=request.message,
        context=request.context,
        current_trip=user_trips.get(session_id)
    )
    
    # If trip planning is needed, invoke trip planner
    trip_plan = None
    if chat_response.requires_planning:
        trip_plan = await trip_planner.plan_trip(
            user_input=request.message,
            preferences=chat_response.extracted_preferences,
            current_trip=user_trips.get(session_id)
        )
        user_trips[session_id] = trip_plan
    
    # Build response
    response = ChatResponse(
        text=chat_response.text,
        trip_plan=trip_plan,
        session_id=session_id,
        timestamp=datetime.now()
    )
    
    # Broadcast updates to all connected clients
    await broadcast_update(response.dict())
    
    return response

@app.post("/optimize")
async def optimize_itinerary(request: Dict[str, Any]):
    """
    Endpoint to re-optimize the itinerary when user makes changes
    """
    session_id = request.get("session_id", "default")
    action = request.get("action")  # "reorder", "remove", "discover"
    data = request.get("data")
    
    current_trip = user_trips.get(session_id)
    if not current_trip:
        return {"error": "No trip found for session"}
    
    # Optimize based on action
    optimized_trip = await optimizer.optimize(
        trip=current_trip,
        action=action,
        action_data=data
    )
    
    user_trips[session_id] = optimized_trip
    
    # Broadcast updated trip
    await broadcast_update({
        "type": "trip_update",
        "trip_plan": optimized_trip.dict(),
        "session_id": session_id
    })
    
    return {"success": True, "trip_plan": optimized_trip}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time updates
    """
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send current trip data if exists
        if session_id in user_trips:
            await websocket.send_json({
                "type": "initial_state",
                "trip_plan": user_trips[session_id].dict()
            })
        
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Process any real-time requests here
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_update(data: Dict[str, Any]):
    """
    Broadcast updates to all connected WebSocket clients
    """
    for connection in active_connections:
        try:
            await connection.send_json(data)
        except:
            # Remove dead connections
            active_connections.remove(connection)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
