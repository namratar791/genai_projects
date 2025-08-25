import os
from dotenv import load_dotenv
from typing import Optional, Dict
# from utils.config.llm_config import getLLM
from utils.config import *
# import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
class RAGPipeline:
    def __init__(self):
        # nothing is loaded multiple times
        self.conversational_rag = RAGConfig.get_conversational_rag()
        self.vector_retriever = RAGConfig.get_vector_retriever()

    def query(self, user_query: str, filter_metadata: Optional[Dict[str, str]] = None):
        # Apply filter dynamically
        # if filter_metadata:
        #     self.vector_retriever.search_kwargs["filter"] = filter_metadata
        result = self.conversational_rag.invoke({"question": user_query})
        return result
    
# rag_pipeline = RAGPipeline()
# result = rag_pipeline.query("What documents are required for a savings account?")
# print("Answer:\n", result["answer"])