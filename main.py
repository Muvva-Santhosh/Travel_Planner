from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import TripRequest, TripResponse
from gemini_client import GeminiClient
from transit_client import TransitClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Travel Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    gemini_client = GeminiClient()
except EnvironmentError as e:
    print(f"Warning: {e}")
    gemini_client = None

transit_client = TransitClient()

@app.get("/")
async def root():
    return {"message": "Travel Planner API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/plan-trip", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    try:
        routes_data = transit_client.get_transit_routes(
            request.origin,
            request.destination
        )
        
        if gemini_client:
            plan = gemini_client.generate_trip_plan(
                request.origin,
                request.destination,
                request.preferences,
                routes_data
            )
        else:
            plan = f"Travel Plan from {request.origin} to {request.destination}\n\nAvailable Routes:\n"
            for i, route in enumerate(routes_data, 1):
                mode = route.get('mode', 'Unknown')
                duration = route.get('duration', 'Unknown')
                cost = route.get('cost', 'Unknown')
                details = route.get('details', 'No details')
                plan += f"\n{i}. {mode} - {duration} - {cost}\n{details}\n"
            plan += "\nNote: AI features are not available. Please set GEMINI_API_KEY environment variable."
        
        return TripResponse(
            plan=plan,
            routes_data=routes_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error planning trip: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
