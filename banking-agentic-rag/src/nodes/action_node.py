from states.banking_state import BankingState


def action_node(state: BankingState):
    try:
      return {"status": "success"}
    except Exception as e:
      return { "response": "error occurred in action_node", "status": "error"}