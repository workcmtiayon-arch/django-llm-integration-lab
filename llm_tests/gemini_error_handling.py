from google.genai import types, errors
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Comment est-ce que je pourrais organiser mes tâches ?",
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )
    print(response.text)
except errors.APIError as exc:
    # Gestion des erreurs renvoyées par l'API Gemini.
    print(f"Erreur d'API Gemini ({exc.code}) : {exc.message}")
except Exception as exc:
    # Gestion d'une erreur de connexion ou d'un délai d'attente dépassé.
    print(f"Erreur inattendue : {exc}")
