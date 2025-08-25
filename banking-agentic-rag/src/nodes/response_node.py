
from states.banking_state import BankingState, SearchResult


def response_node(state: BankingState):
    try:
        collected_text = ""
        

        if state.rag_results:
            collected_text += state.rag_results.content + "\n"
        if state.db_results:
            collected_text += state.db_results.content + "\n"
        if state.web_results:
            collected_text += state.web_results.content + "\n"

        collected_text = collected_text.strip()

        # Update state.response or create a SearchResult object
        state.response = collected_text
        # merged_result = SearchResult(source="Merged", content=collected_text)

        return {"response": collected_text}

    except Exception as e:
        return {"response": "{e}", "status": "error"}