import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Optional fallback or validation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize once
_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY,
)

def getLLM():
    return _llm