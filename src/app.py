from dotenv import load_dotenv
import os   

from google.adk import models as google_models
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
from loguru import logger

load_dotenv()
try:
    gemini_api_key = os.getenv("gemini_api_key")
    attempts = int(os.getenv("attempts", 5))
    exp_base = int(os.getenv("exp_base", 7))
    initial_delay = int(os.getenv("initial_delay", 1))
    http_status_codes = eval(os.getenv("http_status_codes", "[429, 500, 503, 504]"))
 

    retry_config = types.HttpRetryOptions(
        attempts=attempts,
        exp_base=exp_base,
        initial_delay=initial_delay,
        http_status_codes=http_status_codes
    )
    logger.success("Environment variables loaded and retry configuration set successfully.")
except Exception as e:
    logger.error(f"Error loading environment variables: {e} or setting up retry configuration.")
    raise ConnectionError("Failed to load environment variables or set up retry configuration.")


# Agent Definition (agent to answer general questions using Google Search)

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.0-flash-exp",  # ❌ Cambia "gemini-2.5-flash-lite" por este
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)


logger.debug("✅ Root Agent defined.")

runner = InMemoryRunner(agent=root_agent)

logger.debug("✅ Runner created.")

response = await runner.run_debug(
    "What is Agent Development Kit from Google? What languages is the SDK available in?"
)
