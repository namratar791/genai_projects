import asyncio
from states.banking_state import BankingState, SearchResult


async def transaction_node(state: BankingState):
    try:
      if "transactions" in state.intents:
        await asyncio.sleep(0)
        results = SearchResult(source="DB", content=f"Last transaction: -$120 on 2025-08-17", status="success")
        return {"db_results": results}
      else :
        return {"db_results": None}
    except Exception as e:
      results = SearchResult(source="DB", content=f"Error in Transaction", status="error")
      return {"db_results": results}