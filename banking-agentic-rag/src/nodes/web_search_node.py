

import asyncio
from states.banking_state import BankingState, SearchResult

async def web_search_node(state: BankingState):
    try:
        await asyncio.sleep(0)
        results = SearchResult(source="Web", content="External news: bank updated fee schedule", status="success")
        return {"web_results": results}
    except Exception as e:
        results = SearchResult(source="Web", content="Error in Web", status="error")
        return { "web_results": results}