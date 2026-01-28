

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory
from google.genai import types

from dotenv import load_dotenv
import os 
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

async def run_session(runner_instance: Runner, 
                      user_queries: list[str] | str, session_id: str = "default"
                      ):
    """Helper function to run queries in a session and display responses."""
    logger.info(f"\n### Session: {session_id}")

    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

    # Convert single query to list
    if isinstance(user_queries, str):
        user_queries = [user_queries]

    # Process each query
    for query in user_queries:
        print(f"\nUser > {query}")
        query_content = types.Content(role="user", parts=[types.Part(text=query)])

        # Stream agent response
        async for event in runner_instance.run_async(
            user_id=USER_ID, session_id=session.id, new_message=query_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(f"Model: > {text}")

'''
Memory Workflow¶

From the Introduction section, you now know why we need Memory. In order to integrate Memory into your Agents, there are three high-level steps.

Three-step integration process:

    Initialize → Create a MemoryService and provide it to your agent via the Runner
    Ingest → Transfer session data to memory using add_session_to_memory()
    Retrieve → Search stored memories using search_memory()
'''

# Initialize

memory_service = (
    InMemoryMemoryService()
)  # ADK's built-in Memory Service for development and testing



# Define constants used throughout running code
APP_NAME = "MemoryDemoApp"
USER_ID = "demo_user"

# Create agent
user_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="MemoryDemoAgent",
    instruction="Answer user questions in simple words.",
)

logger.info("✅ Agent created")


# Create Session Service 
session_service = InMemorySessionService()  # Handles conversations

# Create runner with BOTH services
runner = Runner(
    agent=user_agent,
    app_name="MemoryDemoApp",
    session_service=session_service,
    memory_service=memory_service,  # Memory service is now available!
)

logger.info("✅ Agent and Runner created with memory support!")

 # Testing Memory

 # User tells agent about their favorite color
await run_session(
    runner,
    "My favorite color is blue-green. Can you write a Haiku about it?",
    "conversation-01",  # Session ID
)

'''
InMemoryMemoryService

    Stores raw conversation events without consolidation
    Keyword-based search (simple word matching)
    In-memory storage (resets on restart)
    Ideal for learning and local development
'''

session = await session_service.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id="conversation-01"
)

# Let's see what's in the session
print("📝 Session contains:")
for event in session.events:
    text = (
        event.content.parts[0].text[:60]
        if event.content and event.content.parts
        else "(empty)"
    )
    print(f"  {event.content.role}: {text}...")



# This is the key method!
await memory_service.add_session_to_memory(session)

logger.success("✅ Session added to memory!")

'''
Add Load Memory Tool to Agent¶

Let's start by implementing the reactive pattern. 
We'll recreate the agent from Section 3, this time 
adding the load_memory tool to its toolkit. Since this 
is a built-in ADK tool, you simply include it in the tools 
array without any custom implementation.'''


# Create agent
user_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="MemoryDemoAgent",
    instruction="Answer user questions in simple words. Use load_memory tool if you need to recall past conversations.",
    tools=[
        load_memory
    ],  # Agent now has access to Memory and can search it whenever it decides to!
)

logger.info("✅ Agent with load_memory tool created.")



# Create a new runner with the updated agent
runner = Runner(
    agent=user_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service,
)

await run_session(runner, "What is my favorite color?", "color-test")


await run_session(runner, "My birthday is on March 15th.", "birthday-session-01")



# Manually save the session to memory
birthday_session = await session_service.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id="birthday-session-01"
)

await memory_service.add_session_to_memory(birthday_session)

logger.info("✅ Birthday session saved to memory!")


# Test retrieval in a NEW session
await run_session(
    runner, "When is my birthday?", "birthday-session-02"  # Different session ID
)

'''
Manual Memory Search¶

Beyond agent tools, you can also search memories directly in your code. This is useful for:

    Debugging memory contents
    Building analytics dashboards
    Creating custom memory management UIs

The search_memory() method takes a text query and returns a SearchMemoryResponse with matching memories.
'''

# Search for color preferences
search_response = await memory_service.search_memory(
    app_name=APP_NAME, user_id=USER_ID, query="What is the user's favorite color?"
)

print("🔍 Search Results:")
print(f"  Found {len(search_response.memories)} relevant memories")
print()

for memory in search_response.memories:
    if memory.content and memory.content.parts:
        text = memory.content.parts[0].text[:80]
        print(f"  [{memory.author}]: {text}...")
'''
Automatic Memory Storage with Callbacks¶

For automatic memory storage, we'll use after_agent_callback. This function triggers every time the agent finishes a turn, then calls add_session_to_memory() to persist the conversation automatically.

But here's the challenge: how does our callback function actually access the memory service and current session? That's where callback_context comes in.

When you define a callback function, ADK automatically passes a special parameter called callback_context to it. The callback_context provides access to the Memory Service and other runtime components.

How we'll use it: In our callback, we'll access the memory service and current session to automatically save conversation data after each turn.

💡 Important: You don't create this context - ADK creates it and passes it to your callback automatically when the callback runs.'''




async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


logger.info ("✅ Callback created.")

'''
Create an Agent: Callback and PreLoad Memory Tool¶

Now create an agent that combines:

    Automatic storage: after_agent_callback saves conversations
    Automatic retrieval: preload_memory loads memories

This creates a fully automated memory system with zero manual intervention.'''



# Agent with automatic memory saving
auto_memory_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="AutoMemoryAgent",
    instruction="Answer user questions.",
    tools=[preload_memory],
    after_agent_callback=auto_save_to_memory,  # Saves after each turn!
)

logger.info("✅ Agent created with automatic memory saving!")

# Create a runner for the auto-save agent
# This connects our automated agent to the session and memory services
auto_runner = Runner(
    agent=auto_memory_agent,  # Use the agent with callback + preload_memory
    app_name=APP_NAME,
    session_service=session_service,  # Same services from Section 3
    memory_service=memory_service,
)

logger.info ("✅ Runner created.")

#  Test 1: Tell the agent about a gift (first conversation)
# The callback will automatically save this to memory when the turn completes
await run_session(
    auto_runner,
    "I gifted a new toy to my nephew on his 1st birthday!",
    "auto-save-test",
)

# Test 2: Ask about the gift in a NEW session (second conversation)
# The agent should retrieve the memory using preload_memory and answer correctly
await run_session(
    auto_runner,
    "What did I gift my nephew?",
    "auto-save-test-2",  # Different session ID - proves memory works across sessions!
)

'''
How often should you save Sessions to Memory?¶

Options:
Timing 	                Implementation 	                Best For
After every turn 	    after_agent_callback 	        Real-time memory updates
End of conversation 	Manual call when session ends 	Batch processing, reduce API calls
Periodic intervals 	    Timer-based background job 	    Long-running conversationsThe Limitation of Raw Storage¶

What we've stored so far:

    Every user message
    Every agent response
    Every tool call

The problem:

Session: 50 messages = 10,000 tokens
Memory:  All 50 messages stored
Search:  Returns all 50 messages → Agent must process 10,000 tokens

This doesn't scale. We need consolidation.

Summary

You've learned the core mechanics of Memory in ADK:

    ✅ Adding Memory
        Initialize MemoryService alongside SessionService
        Both services are provided to the Runner

    ✅ Storing Information
        await memory_service.add_session_to_memory(session)
        Transfers session data to long-term storage
        Can be automated with callbacks

    ✅ Searching Memory
        await memory_service.search_memory(app_name, user_id, query)
        Returns relevant memories from past conversations

    ✅ Retrieving in Agents
        Reactive: load_memory tool (agent decides when to use memory)
        Proactive: preload_memory tool (always loads memory into LLM's system instructions)

    ✅ Memory Consolidation
        Extracts key information from Session data
        Provided by managed memory services such as Vertex AI Memory Bank

🎉 Congratulations! You've learned Memory Management in ADK!
'''

