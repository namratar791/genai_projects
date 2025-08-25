from utils.llm.llm import getLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
from utils.prompts.prompt_loader import load_prompt_folder
from states.CCTNSState import CCTNSState

_llm = getLLM()
prompts = load_prompt_folder("prompt_translate_to_selected_language.txt")
prompt = translation_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", prompts),
        ("human", "{query}")
    ]
)
parser = JsonOutputParser()
chain = prompt | _llm | parser
def translate_response(state: CCTNSState):
    # original_text = state.get("t", "")
    
    try:
        selected_language = state.get("selected_language","")
        next_prompt = state.get("next_prompt","")
        result = chain.invoke({
            "selected_language": selected_language,
            "query": next_prompt
        })  # Telugu: "This is a good day."
        print(result)
        return {
            "status": "success",
            "final_response": result["response"],
            "selected_language": selected_language,
            "error": None
        }
    except Exception as e:
        print(f"{e} exception in english")
        return {
            "status": "error",
            "error": f"Translation failed: {str(e)}",
            "final_response": None
        }

        