# AI Travel Planner

An intelligent travel planning application that uses conversational AI to create personalized itineraries. Built with React.js, FastAPI, and LangChain, featuring real-time updates and interactive maps.

![AI Travel Planner](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)

## Features

- **Conversational AI Interface**: Chat with an AI assistant to plan your trips
- **Interactive Map**: Visual representation of your itinerary with Google Maps
- **Real-time Updates**: WebSocket integration for instant updates
- **Smart Itinerary Management**: Add, remove, and reorder activities
- **Multi-model AI**: Supports both OpenAI and Anthropic models
- **Responsive Design**: Built with Mantine UI components

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                    │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Chat Interface │    Google Map   │   Itinerary Display     │
│                 │                 │                         │
└────────┬────────┴────────┬────────┴────────┬────────────────┘
         │                 │                 │
         └─────────────────┴─────────────────┘
                           │
                    WebSocket + REST API
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    Backend (FastAPI)                        │
├─────────────────────────────────────────────────────────────┤
│                   LangChain Agents                          │
├─────────────┬──────────────┬────────────────────────────────┤
│ Chat Agent  │ Trip Planner │   Itinerary Optimizer          │
└─────────────┴──────────────┴────────────────────────────────┘
```

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- API Keys:
  - OpenAI API Key
  - Anthropic API Key
  - Google Maps API Key

## Quick Start

### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-travel-planner
```

2. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment template and add your API keys:
```bash
cp env.example .env
# Edit .env with your API keys
```

5. Run the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. In a new terminal, navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_key_here
```

4. Start the development server:
```bash
npm start
```

## Usage

1. **Start a Conversation**: Type a message in the chat interface about where you'd like to travel.

2. **Provide Details**: The AI will ask for your preferences, dates, and interests.

3. **View Your Itinerary**: Once planned, your trip will appear on the map and in the itinerary panel.

4. **Customize Your Trip**:
   - Click on map markers for attraction details
   - Remove activities with the trash icon
   - Reorder or discover new places from the menu

## Project Structure

```
DATASCI-210-06-2025-AI-Trip-Planner/
├── backend/
│   ├── agents/           # LangChain agent implementations
│   │   ├── chat_agent.py
│   │   ├── trip_planner.py
│   │   └── optimizer.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── store/       # Redux store and slices
│   │   ├── services/    # API and WebSocket services
│   │   └── types/       # TypeScript definitions
│   ├── public/
│   └── package.json
├── docker-compose.yml
└── README.md
```

## API Endpoints

### REST Endpoints

- `POST /chat` - Send a message to the AI assistant
  ```json
  {
    "message": "I want to visit San Francisco",
    "session_id": "session-123",
    "context": {}
  }
  ```

- `POST /optimize` - Optimize or modify the itinerary
  ```json
  {
    "session_id": "session-123",
    "action": "remove|reorder|discover",
    "data": {}
  }
  ```

### WebSocket

- `ws://localhost:8000/ws/{session_id}` - Real-time updates for trip changes

## Configuration

### Backend Configuration

The backend can be configured through environment variables:

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `APP_ENV` - Application environment (development/production)
- `LOG_LEVEL` - Logging level (INFO/DEBUG/ERROR)

### Frontend Configuration

- `REACT_APP_API_URL` - Backend API URL
- `REACT_APP_WS_URL` - WebSocket URL
- `REACT_APP_GOOGLE_MAPS_API_KEY` - Google Maps API key

## Development

### Adding New Agents

1. Create a new agent in `backend/agents/`
2. Implement the agent logic using LangChain
3. Integrate with the main application in `main.py`

### Modifying the UI

1. Components are in `frontend/src/components/`
2. Redux state management in `frontend/src/store/`
3. Use Mantine UI components for consistency

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

See [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md) for detailed deployment instructions including:
- AWS ECS deployment
- EC2 deployment
- AWS App Runner setup

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure the backend CORS settings match your frontend URL
2. **WebSocket connection failed**: Check that the WebSocket URL is correct
3. **Google Maps not loading**: Verify your API key has the necessary permissions

### Logs

- Backend logs: `docker-compose logs backend`
- Frontend logs: `docker-compose logs frontend`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [LangChain](https://langchain.com/) for AI orchestration
- Maps integration via [Google Maps API](https://developers.google.com/maps)

## Future Enhancements

- [ ] User authentication and saved trips
- [ ] Integration with booking APIs
- [ ] Weather information
- [ ] Budget tracking
- [ ] Collaborative trip planning
- [ ] Mobile app version
