from google.genai import types, errors
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
try:
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

except errors.ClientError as exc:
    if exc.code == 429:
        print(
            "Erreur : le quota Gemini est dépassé. "
            "Veuillez réessayer après le renouvellement du quota."
        )
    else:
        print(f"Erreur d'API Gemini ({exc.code}) : {exc.message}")
except errors.APIError as exc:
    print(f"Erreur d'API Gemini ({exc.code}) : {exc.message}")
except Exception as exc:
    print(f"Erreur inattendue : {exc}")
