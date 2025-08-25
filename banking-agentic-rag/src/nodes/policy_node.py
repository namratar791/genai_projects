import asyncio
from states.banking_state import BankingState, SearchResult
from rag.rag_pipeline import RAGPipeline

def policy_node(state: BankingState):
    """
    LangGraph node to handle policy queries.
    Returns a dictionary with 'policy_response' key containing a PolicyResponse instance.
    """
    # retries = 2
    # print("inside rag.....")
    # for attempt in range(retries):
    try:
        intents = getattr(state, "intents", [])  # or state.intents

        if "policy" in intents:
            query = getattr(state, "user_query", "")
            rag_pipeline = RAGPipeline()
            result = rag_pipeline.query(query)
            resp_policy = result["answer"]
            results = SearchResult(source="RAG", content=f"{resp_policy}", status="success")
            return {"rag_results": results}
        else:
            return {"rag_results": None}
        # return { "policy_response": policy_resp}
    except Exception as e:
        results = SearchResult(source="RAG", content=f"{e}", status="error")
        return { "rag_results": results}



    # rag_pipeline = RAGPipeline()  # singleton
    # retries = 2
    # print("inside rag.....")
    # for attempt in range(retries):
    #     try:
    #         result = await rag_pipeline.query(state.user_query)
    #         resp_policy = result["answer"]
    #         # print(f"----result-----{result['answer']}")
    #         print("Answer:\n", result["answer"])
    #         results = SearchResult(source="RAG", content=resp_policy, status="success")
    #         print("SearchResult Object:", results.json())
    #         return {"rag_results": results}
    #     except Exception as e:
    #         if attempt == retries - 1:
    #             return {"rag_results": None, "error": str(e)}
    #         await asyncio.sleep(1)  # backoff