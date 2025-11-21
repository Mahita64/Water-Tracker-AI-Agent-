import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from google import genai
from src.database import log_intake, get_intake
from datetime import datetime

load_dotenv()

GOOGLE_API = os.getenv("GOOGLE_API")
gemini_client = genai.Client(api_key=GOOGLE_API)



class WaterAgent:

    def __init__(self):
        self.history = []
    
    def analyze(self, user_id):

        history = get_intake(user_id)
        today = datetime.today().strftime("%Y-%m-%d")
        todays_amounts = [
            row[0] for row in history if row[1] == today
        ]

        total_intake_today = sum(todays_amounts) if todays_amounts else 0

        prompt = f"""You are a hydration assitant. 
        The user will present you their consumed ml of water today.
        Provide a hydration status (keep it short in 1 sentence) and suggest if they have to drink more water (Keep short again with 1-2 sentences).
        Start the response with (You Drank ___ ml today.) and then the status and suggestion"""

        message = [
            (
                "system", prompt
            ),
            (
                "human", str(total_intake_today)
            )
        ]
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )

        return response.text

if __name__ == "__main__":
    agent = WaterAgent()

