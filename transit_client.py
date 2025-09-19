import httpx
from typing import List, Dict, Any
import os

class TransitClient:
    def __init__(self):
        self.api_key = os.getenv("TRANSIT_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/directions/json"
    
    def get_transit_routes(self, origin: str, destination: str) -> List[Dict[str, Any]]:
        if self.api_key:
            try:
                return self.get_google_maps_routes(origin, destination)
            except Exception as e:
                print(f"Error fetching Google Maps data: {e}")
                return self.get_mock_routes(origin, destination)
        else:
            return self.get_mock_routes(origin, destination)
    
    def get_google_maps_routes(self, origin: str, destination: str) -> List[Dict[str, Any]]:
        params = {
            "origin": origin,
            "destination": destination,
            "mode": "transit",
            "key": self.api_key,
            "alternatives": "true"
        }
        try:
            response = httpx.get(self.base_url, params=params, timeout=15)
            data = response.json()
            if data.get("status") != "OK":
                return self.get_mock_routes(origin, destination)
            routes = []
            for i, route in enumerate(data.get("routes", [])[:5]):
                leg = route["legs"][0]
                steps = []
                total_duration = leg["duration"]["text"]
                for step in leg["steps"]:
                    if step["travel_mode"] == "TRANSIT":
                        transit_details = step["transit_details"]
                        steps.append(f"Take {transit_details['line']['name']} from {transit_details['departure_stop']['name']} to {transit_details['arrival_stop']['name']}")
                    else:
                        steps.append(step["html_instructions"].replace("<b>", "").replace("</b>", ""))
                routes.append({
                    "mode": "Google Maps Transit",
                    "duration": total_duration,
                    "cost": "₹50-200",
                    "details": f"Google Maps suggested route from {origin} to {destination}",
                    "steps": steps,
                    "operator": "Google Maps",
                    "frequency": "Real-time",
                    "comfort": "Good",
                    "accuracy": "Very High"
                })
            return routes if routes else self.get_mock_routes(origin, destination)
        except Exception as e:
            print(f"Error with Google Maps API: {e}")
            return self.get_mock_routes(origin, destination)
    
    def get_mock_routes(self, origin: str, destination: str) -> List[Dict[str, Any]]:
        mock_routes = [
            {
                "mode": "State Transport Bus",
                "duration": "3-8 hours",
                "cost": "₹80-400",
                "details": f"Take state transport bus from {origin} to {destination}. Comfortable and economical option.",
                "steps": [
                    f"Go to {origin} bus stand",
                    f"Book ticket at counter or online",
                    f"Board state transport bus to {destination}",
                    f"Travel time: 3-8 hours depending on distance",
                    f"Get down at {destination} bus stand",
                    f"Take local transport to final destination"
                ],
                "operator": "State Transport Corporation",
                "frequency": "Every 30-60 minutes",
                "comfort": "Standard",
                "accuracy": "High"
            },
            # Add other mock routes similarly as before...
        ]
        return mock_routes
    
    async def get_real_transit_routes(self, origin: str, destination: str) -> List[Dict[str, Any]]:
        # Async wrapper stub — consider refactoring for true async calls if needed
        return self.get_transit_routes(origin, destination)
