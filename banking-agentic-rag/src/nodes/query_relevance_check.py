
from states.banking_state import BankingState
from utils.config import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate

llm = LLMConfig.getLLM()

parser = JsonOutputParser()
# llm = getLLM()
prompts = """
    You are a Banking Triage Router Assistant.  
    Classify the user query into:  
    - relevance: one of ["in_scope", "out_of_scope", "clarify"]  
    - intents: a list containing any of ["policy", "transaction", "actions"]  

    Rules:  
    - Add "policy" if the query involves policy, fee schedules, disputes, KYC, or similar.  
    - Add "transactions" if the query involves past or recent transactions.  
    - Add "actions" if the query requests an action (e.g., freeze card, cancel card, report fraud, dispute).  

    Output:  
    Return only a JSON object in the following format, with no extra text or explanation:  

    {{
        "relevance" : "<in_scope | out_of_scope | clarify>",
        "intents" : ["<policy|transactions|actions if any, empty if None>"]
    }}
"""
prompt = chat_prompt = ChatPromptTemplate.from_messages([
("system", prompts),
("human", "{query}")
])
chain = prompt | llm | parser

def query_relevance_check(state: BankingState):
    # user_query = state.get("user_query", "")
    try:
      response = chain.invoke({"query": state.user_query}) 
      intents = response.get('intents', []) 
      print(f"{response.get('intents', [])}....jhjkhu.") 
      return {"status": "success", "intents": intents}
      # return {"status": "success", "intents": resp_dict}
    except Exception as e:
      return { "response": "error occurred in voice_to_text", "status": "error"}
    


