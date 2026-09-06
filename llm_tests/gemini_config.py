from google.genai import types
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Bonjour comment organiser mes taches en semaines et en mois ?",
    config=types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        temperature=0.9,
        max_output_tokens=2000,
        system_instruction=(
            "Tu es un assistant qui aide à organiser les taches en semaines et en mois. reponds de facon concise et actionnable"
        ),
    ),
)

print(response.text)
