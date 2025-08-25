
from states.banking_state import BankingState


def router_node(state: BankingState):
    try:
      return {"status": "success"}
    except Exception as e:
      return { "response": "error occurred in router_node", "status": "error"}