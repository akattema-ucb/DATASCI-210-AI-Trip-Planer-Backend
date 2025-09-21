from typing import Dict, Any, Optional
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class ChatAgentResponse(BaseModel):
    text: str
    requires_planning: bool = False
    extracted_preferences: Optional[Dict[str, Any]] = None

class ChatAgent:
    """
    Main conversational agent that handles user interactions
    and determines when trip planning is needed
    """
    
    def __init__(self):
        # Initialize both OpenAI and Anthropic models
        self.openai_model = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.anthropic_model = ChatAnthropic(
            model="claude-3-opus-20240229",
            temperature=0.7,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        self.system_prompt = """You are a friendly and knowledgeable AI travel assistant. 
        Your goal is to help users plan amazing trips. You should:
        1. Engage in natural conversation about travel preferences
        2. Extract key information like destinations, dates, interests, and budget
        3. Determine when the user is ready for a detailed trip plan
        4. Provide helpful suggestions and local insights
        
        When you detect the user wants to plan a specific trip, set requires_planning=True
        and extract their preferences into a structured format."""
    
    async def process_message(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None,
        current_trip: Optional[Any] = None
    ) -> ChatAgentResponse:
        """
        Process user message and determine response strategy
        """
        # TODO: Implement actual LangChain conversation logic
        # This is a placeholder implementation
        
        # For now, return a mock response
        # Check if message contains trip planning keywords
        planning_keywords = ["plan", "trip", "itinerary", "visit", "travel to", "going to"]
        requires_planning = any(keyword in message.lower() for keyword in planning_keywords)
        
        # Mock response based on message content
        if "san francisco" in message.lower() or "sf" in message.lower():
            response_text = """I'd be happy to help you plan a trip to San Francisco! 
            The Bay Area has so much to offer - from the iconic Golden Gate Bridge to 
            the vibrant neighborhoods like Mission District and Chinatown. 
            
            To create the perfect itinerary, could you tell me:
            - How many days are you planning to stay?
            - What are your main interests? (food, culture, nature, tech, etc.)
            - Do you have a budget in mind?"""
            
            extracted_preferences = {
                "destination": "San Francisco",
                "interests": ["sightseeing", "food", "culture"],
                "duration_days": 3  # Default assumption
            }
        else:
            response_text = "I'm your AI travel assistant! Where would you like to explore?"
            extracted_preferences = None
        
        return ChatAgentResponse(
            text=response_text,
            requires_planning=requires_planning,
            extracted_preferences=extracted_preferences
        )
