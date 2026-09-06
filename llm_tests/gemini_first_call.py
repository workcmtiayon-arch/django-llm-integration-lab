import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

"""Pour charger les variables d'environnement a partir du fichier .env"""
load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Bonjour, ça va ?",
    config=types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        )
    )
)

print(response.text)
