import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from schemas import TaskAnalysis


load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Voici mes tâches : ... Analyse-les et propose des priorités.",
    config=types.GenerateContentConfig(
        temperature=0.2,
        response_mime_type="application/json",
        response_schema=TaskAnalysis,
    ),
)

# response.parsed est déjà une instance validée de TaskAnalysis
analysis: TaskAnalysis = response.parsed
for suggestion in analysis.suggestions:
    print(suggestion.title, suggestion.priority)
