import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from google import genai


load_dotenv()

GOOGLE_API = os.getenv("GOOGLE_API")
gemini_client = genai.Client(api_key=GOOGLE_API)



class WaterAgent:

    def __init__(self):
        self.history = []
    
    def analyze(self, intake_ml):

        prompt = f"""You are a hydration assitant. 
        The user will present you their consumed ml of water today.
        Provide a hydration status (keep it short in 1 sentence) and suggest if they have to drink more water (Keep short again with 1-2 sentences)."""

        message = [
            (
                "system", prompt
            ),
            (
                "human", str(intake_ml)
            )
        ]
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )

        return response.text

if __name__ == "__main__":
    agent = WaterAgent()
    intake = 500
    feedback = agent.analyze(intake)
    
    print(feedback)
