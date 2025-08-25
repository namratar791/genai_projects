import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from states.CCTNSState import CCTNSState
from openai import OpenAI  # New official client from latest openai python SDK
from utils.llm.llm import getLLM
from langchain_core.output_parsers import StrOutputParser
from utils.prompts.prompt_loader import load_prompt_folder
from langchain.prompts import ChatPromptTemplate

parser = StrOutputParser()
llm = getLLM()
prompts = load_prompt_folder("check_query_completeness/prompt.txt")
prompt = chat_prompt = ChatPromptTemplate.from_messages([
("system", prompts)
])
chain = prompt | llm | parser
def check_query_completeness( state: CCTNSState) :
    try:
        result = chain.invoke({})
        print(f"{result}\n")
        user_input = input("Please enter Y/N to continue or exit: ").strip().lower()

        if user_input == 'y':
            print("✅ Continuing...")
        elif user_input == 'n':
            print("👋 Exiting...")
        else:
            print("❌ Invalid input. Please enter 'Y' or 'N'.")
        return {"status": "success"}
    except:
        return { "error": "error occurred in voice_to_text", "status": "error"}