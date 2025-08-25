import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from utils.llm.llm import getLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
from utils.prompts.prompt_loader import load_prompt_folder
from states.CCTNSState import CCTNSState
from utils.logger import logger

# Initialize once

# chain = prompt | llm | parser

_llm = getLLM()
prompts = load_prompt_folder("prompt_translate_to_english.txt")
prompt = translation_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", prompts),
        ("human", "{query}")
    ]
)
parser = JsonOutputParser()
chain = prompt | _llm | parser
def translate_to_english(state: CCTNSState) -> dict:
    original_text = state.get("user_query", "")
    
    if not original_text:
        print(f"translated text: error ")
        return {
            "status": "error",
            "error": "No transcribed text to translate.",
        }

    try:
        response = chain.invoke({"query": original_text})  # Telugu: "This is a good day."

        print(response)
        return {
            "status": "success",
            "translated_text": response["translation"],
            "selected_language": response["language"],
            "error": None
        }
    except Exception as e:
        logger.info(f"{e} exception in english")
        return {
            "status": "error",
            "error": f"Translation failed: {str(e)}",
            "selected_language": None,
            "translated_text": None
        }
