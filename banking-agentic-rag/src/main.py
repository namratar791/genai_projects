import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from openai import OpenAI  # New official client from latest openai python SDK
from agents.banking_agent import run_banking_agent
from utils.config import *

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)



async def run():
    # setup_db()
    memory = MemoryConfig.get_memory()  # Singleton memory

    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        # Store user message in conversation memory
        memory.chat_memory.add_user_message(query)
        workflow = run_banking_agent()
        result_invoke = await workflow.ainvoke({"user_query":query})
        print(result_invoke)
        final_response = result_invoke["response"]
        memory.chat_memory.add_ai_message(final_response)
        print(final_response)

asyncio.run(run())