import os
from dotenv import load_dotenv
from google import genai

"""Pour charger les variables d'environnement a partir du fichier .env"""
load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Salut gar... donne moi un conseil sur comment etre un bon developpeur frontend dont la biblio principale est le REACT stp."
)

print(response.text)
