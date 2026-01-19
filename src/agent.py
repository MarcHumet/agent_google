# agent.py (guarda en ~/project/agents/agent_google/agent.py)

from loguru import logger   

from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search 

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(model="gemini-2.5-flash-lite-preview-09-2025"),  # Tu modelo correcto  # ✅ 15 RPM gratis
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info.",
    tools=[google_search],
)
logger.debug("✅ Root Agent defined.") 

# No Funcionan
# ✅ gemini-2.0-flash-lite-001
# ✅ gemini-2.0-flash-lite
# ✅ gemini-2.0-flash-lite-preview-02-05
# ✅ gemini-2.0-flash-lite-preview
# ✅ gemini-2.5-flash-lite-preview-09-2025


#Modelos testeados que funcionan con ASK modealidad gratuita:

# ✅ gemini-flash-lite-latest
# ✅ gemini-2.5-flash-lite
# ✅ gemini-2.5-flash
# #
# # En notebook/celda
# import google.generativeai as genai
# genai.configure(api_key="AIzaSyDHxutmX5cjUJ3bPEu23aRW9b6SESnHdAs")
# for m in genai.list_models():
#     name = m.name.split('/')[-1]
#     if 'generateContent' in m.supported_generation_methods and 'lite' in name.lower():
#         print(f"✅ {name}")



# import google.generativeai as genai

# for m in genai.list_models():
#     print(m.name, m.supported_generation_methods)

#     models/embedding-gecko-001 ['embedText', 'countTextTokens']
# models/gemini-2.5-flash ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.5-pro ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.0-flash-exp ['generateContent', 'countTokens', 'bidiGenerateContent']
# models/gemini-2.0-flash ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.0-flash-001 ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.0-flash-lite-001 ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.0-flash-lite ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.0-flash-lite-preview-02-05 ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.0-flash-lite-preview ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-exp-1206 ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.5-flash-preview-tts ['countTokens', 'generateContent']
# models/gemini-2.5-pro-preview-tts ['countTokens', 'generateContent', 'batchGenerateContent']
# models/gemma-3-1b-it ['generateContent', 'countTokens']
# models/gemma-3-4b-it ['generateContent', 'countTokens']
# models/gemma-3-12b-it ['generateContent', 'countTokens']
# models/gemma-3-27b-it ['generateContent', 'countTokens']
# models/gemma-3n-e4b-it ['generateContent', 'countTokens']
# models/gemma-3n-e2b-it ['generateContent', 'countTokens']
# models/gemini-flash-latest ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-flash-lite-latest ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-pro-latest ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.5-flash-lite ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.5-flash-image ['generateContent', 'countTokens', 'batchGenerateContent']
# models/gemini-2.5-flash-preview-09-2025 ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-2.5-flash-lite-preview-09-2025 ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-3-pro-preview ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-3-flash-preview ['generateContent', 'countTokens', 'createCachedContent', 'batchGenerateContent']
# models/gemini-3-pro-image-preview ['generateContent', 'countTokens', 'batchGenerateContent']
# models/nano-banana-pro-preview ['generateContent', 'countTokens', 'batchGenerateContent']
# models/gemini-robotics-er-1.5-preview ['generateContent', 'countTokens']
# models/gemini-2.5-computer-use-preview-10-2025 ['generateContent', 'countTokens']
# models/deep-research-pro-preview-12-2025 ['generateContent', 'countTokens']
# models/embedding-001 ['embedContent']
# models/text-embedding-004 ['embedContent']
# models/gemini-embedding-exp-03-07 ['embedContent', 'countTextTokens', 'countTokens']
# models/gemini-embedding-exp ['embedContent', 'countTextTokens', 'countTokens']
# models/gemini-embedding-001 ['embedContent', 'countTextTokens', 'countTokens', 'asyncBatchEmbedContent']
# models/aqa ['generateAnswer']
# models/imagen-4.0-generate-preview-06-06 ['predict']
# models/imagen-4.0-ultra-generate-preview-06-06 ['predict']
# models/imagen-4.0-generate-001 ['predict']
# models/imagen-4.0-ultra-generate-001 ['predict']
# models/imagen-4.0-fast-generate-001 ['predict']
# models/veo-2.0-generate-001 ['predictLongRunning']
# models/veo-3.0-generate-001 ['predictLongRunning']
# models/veo-3.0-fast-generate-001 ['predictLongRunning']
# models/veo-3.1-generate-preview ['predictLongRunning']
# models/veo-3.1-fast-generate-preview ['predictLongRunning']
# models/gemini-2.5-flash-native-audio-latest ['countTokens', 'bidiGenerateContent']
# models/gemini-2.5-flash-native-audio-preview-09-2025 ['countTokens', 'bidiGenerateContent']
# models/gemini-2.5-flash-native-audio-preview-12-2025 ['countTokens', 'bidiGenerateContent']