import google.generativeai as genai
import os
from typing import Dict, Any, List

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY environment variable is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_trip_plan(
        self,
        origin: str,
        destination: str,
        preferences: Dict[str, Any],
        routes_data: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a comprehensive trip plan using Gemini AI.
        """
        routes_text = ""
        for i, route in enumerate(routes_data, 1):
            mode = route.get('mode', 'Unknown')
            details = route.get('details', 'No details')
            duration = route.get('duration', None)
            cost = route.get('cost', None)
            routes_text += f"Route {i}: {mode} - {details}\n"
            if duration:
                routes_text += f"  Duration: {duration}\n"
            if cost:
                routes_text += f"  Cost: {cost}\n"
            routes_text += "\n"
        
        prompt = (
            f"You are a helpful travel assistant specializing in India. Based on the following information, create a comprehensive travel plan:\n\n"
            f"Origin: {origin}\n"
            f"Destination: {destination}\n"
            f"User Preferences: {preferences}\n\n"
            f"Available Public Transport Routes:\n{routes_text}\n"
            "Please provide a detailed travel plan that includes:\n"
            "1. Route Recommendations: Suggest the best route based on user preferences (budget, time, comfort)\n"
            "2. Step-by-Step Instructions: Clear directions for each recommended route\n"
            "3. India-Specific Tips:\n"
            "   - Best times to travel (avoiding peak hours and rush times)\n"
            "   - Local transport connections (auto, share auto, local buses)\n"
            "   - Important landmarks and transport hubs\n"
            "   - Weather considerations and seasonal factors\n"
            "   - Cultural sites to visit along the way\n"
            "   - Regional language phrases that might be helpful\n"
            "4. Cost Breakdown: Detailed cost analysis in Indian Rupees (₹)\n"
            "5. Safety Tips: Important safety considerations for travelers in India\n"
            "6. Alternative Options: Backup plans if primary route is not available\n"
            "7. Local Insights:\n"
            "   - Best places to eat near transport hubs\n"
            "   - Local customs and etiquette\n"
            "   - Emergency contacts and helpline numbers\n"
            "   - Mobile network coverage areas\n"
            "8. Accessibility Information: If user has accessibility needs\n"
            "9. Booking Information:\n"
            "   - How to book tickets online (IRCTC, redBus, etc.)\n"
            "   - Advance booking requirements\n"
            "   - Cancellation policies\n"
            "10. Real-time Updates:\n"
            "   - How to check for delays and cancellations\n"
            "   - Live tracking options\n"
            "   - Customer service contacts\n"
            "Make the response practical, culturally aware, and specific to Indian travel. Use a friendly, helpful tone and include emojis to make it engaging. Focus on accuracy and reliability of information."
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error generating trip plan: {str(e)}")
