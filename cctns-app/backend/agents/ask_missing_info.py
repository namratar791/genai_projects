
from utils.llm.llm import getLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
from utils.prompts.prompt_loader import load_prompt_folder
from states.CCTNSState import CCTNSState
from utils.logger import logger
# Initialize once

# chain = prompt | llm | parser

__llm = getLLM()

prompts = template = """
{{
  "query_status": "<complete | incomplete>",
  "missing_fields": ["<field_names if any, empty if none>"],
  "relevant_fields": {{
    "location": "<extracted location or null>",
    "crime_type": "<found or null>",
    "date_registered": "<found or null>",
    "status": "<found or null>"
  }},
  "next_prompt": "<If incomplete, ask for missing location and give some suggestion like try to end your query with a location, for example: 'guntur location'; if complete, say: 'Processing your request...'>"
}}

You are an assistant that checks whether a user's query is complete with respect to location (anywhere in the world) and valid for retrieving FIR case details.

You only consider data from the following:
- Table: fir
- Fields: crime_type, location (mandatory), date_registered (format: YYYY-MM-DD), status

Extraction rules:
1. Location is mandatory — look for it explicitly.
2. Recognize a location if it appears after words like 'in', 'at', 'from', 'near', 'around'.
3. Capture all words after the preposition until you hit punctuation or the sentence ends.
4. crime_type: detect keywords like 'theft', 'robbery', 'murder', 'fraud', 'assault'.
5. date_registered: detect exact YYYY-MM-DD format.
6. status: detect 'open', 'closed', 'pending', 'under investigation'.
7. If location missing, mark incomplete and check if the query is related to FIR details
   if its relevant to the context then ask for next_prompt with location details
   if its not relevant to the context then ask for next_prompt with Please ask queries related to CCTNS FIR details
8. If location is mentioned, mark the status as complete and don't ask for optional fields.

Examples:

User query: "Show all open cases in Sangareddy town."

Response:
{{
  "query_status": "complete",
  "missing_fields": [],
  "relevant_fields": {{
    "location": "Sangareddy town",
    "crime_type": null,
    "date_registered": null,
    "status": "open"
  }},
  "next_prompt": "Processing your request..."
}}

User query: "Show all cases in the Guntur region."

Response:
{{
  "query_status": "complete",
  "missing_fields": [],
  "relevant_fields": {{
    "location": "Guntur",
    "crime_type": null,
    "date_registered": null,
    "status": null
  }},
  "next_prompt": "Processing your request..."
}}

User query: "list robbery cases from 2024-07-01"

Response:
{{
  "query_status": "incomplete",
  "missing_fields": ["location"],
  "relevant_fields": {{
    "location": null,
    "crime_type": "robbery",
    "date_registered": "2024-07-01",
    "status": null
  }},
  "next_prompt": "Please provide the location.For example: 'Show me all the open cases in ABC location'."
}}

"""

prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", prompts),
        ("human", "{query}")
    ]
)

parser = JsonOutputParser()

chain = prompt | __llm | parser

def ask_missing_info(state: CCTNSState) -> dict:
    original_text = state.get("translated_text", "")
    
    logger.info(f"ask_missing_info input: {original_text}")
    
    if not original_text:
        logger.error("No translated_text found in state")
        return {
            "status": "error",
            "error": "No translated_text found in state",
            "is_complete": None,
            "next_prompt": None
        }
    
    try:
        # invoke chain with the query text
        response = chain.invoke({"query": original_text})
        
        # Optionally log the full response
        logger.info(f"ask_missing_info response: {response}")
        
        selected_language = state.get("selected_language", "")
        
        return {
            "status": "success",
            "is_complete": response.get("query_status", None),
            "next_prompt": response.get("next_prompt", None),
            "selected_language": selected_language,
            "error": None
        }
    except Exception as e:
        logger.error(f"ask_missing_info exception: {str(e)}")
        return {
            "status": "error",
            "error": f"ask_missing_info failed: {str(e)}",
            "is_complete": None,
            "next_prompt": None
        }
