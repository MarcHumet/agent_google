from dotenv import load_dotenv
import os     




from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

load_dotenv()

gemini_api_key = os.getenv("gemini_api_key")
print("Gemini API Key:", gemini_api_key)    

