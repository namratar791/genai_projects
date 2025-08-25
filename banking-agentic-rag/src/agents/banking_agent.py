from langgraph.graph import StateGraph, END
from nodes import *
from states.banking_state import BankingState

def exception_handler(state: BankingState):
    error_txt = state.get("error","")
    return {}

def route_policy(s): return "policy_node" if "policy" in s.intents else END

def run_banking_agent():
    graph = StateGraph(BankingState)
    # query_relevance_check()
    graph.add_node("query_relevance_check", query_relevance_check)
    graph.add_node("policy_node_search", policy_node)
    graph.add_node("transaction_node_search", transaction_node )
    graph.add_node("sentiment_node", sentiment_node )
    # graph.add_node("action_node", action_node )
    # graph.add_node("router_node", router_node )
    graph.add_node("merger_node", response_node)
    

    graph.set_entry_point("query_relevance_check")
    # graph.add_edge("query_relevance_check", "router_node")
    graph.add_edge("query_relevance_check", "policy_node_search")
    graph.add_edge("query_relevance_check", "transaction_node_search")
    graph.add_edge("policy_node_search", "merger_node")
    graph.add_edge("transaction_node_search", "merger_node")
    graph.add_edge("merger_node", "sentiment_node")
    # graph.add_edge("merger_node","sentiment_node")
    # graph.add_edge("sentiment_node", "merger_node" )
    graph.set_finish_point("sentiment_node")

    workflow = graph.compile()
    return workflow


