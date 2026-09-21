import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from schemas import TaskAnalysis


load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
