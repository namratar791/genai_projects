import os

from dotenv import load_dotenv
from states.CCTNSState import CCTNSState
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm.llm import getLLM
from utils.prompts.prompt_loader import load_prompt_folder

llm = getLLM()
prompts = load_prompt_folder("text_to_sql/prompt.txt")
prompt = chat_prompt = ChatPromptTemplate.from_messages([
("system", prompts),
("human", "{query}")
])

# parser = PydanticOutputParser(pydantic_object=UserInputSchema)
parser = StrOutputParser()
chain = prompt | llm | parser
def text_to_sql( state: CCTNSState) :
    try:
        translated_text = state.get("translated_text","")
        result = chain.invoke({"query": translated_text})
        sql_query = " ".join(result.split())
        if "irrelevant" in sql_query.lower():
            # print("Input is irrelevant........")
            return { "error": "Input is irrelevant", "status": "error", "db_results": []}
        else:
            print(f"Input is relevant.{sql_query}")
            return {"status": "success", "sql_query": sql_query}
    except:
        return { "error": "error occurred in text_to_sql", "status": "error"}