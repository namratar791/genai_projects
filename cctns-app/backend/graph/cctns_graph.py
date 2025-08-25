from langgraph.graph import StateGraph, END
from states.CCTNSState import CCTNSState
from agents import *


def exception_handler(state: CCTNSState):
    error_txt = state.get("error","")
    print(f"{error_txt}.....")
    return {}

def run_cctns_agent():
    graph = StateGraph(CCTNSState)
    # graph.add_node("voice_to_text", voice_to_text)
    # # graph.add_node("ask_more_info", voice_to_text)
    # graph.add_node("text_to_sql", text_to_sql)
    # graph.add_node("execute_sql", execute_sql)
    # # graph.add_node("generate_report", generate_report)
    # graph.add_node("exception_handler", exception_handler)

    # graph.set_entry_point("voice_to_text")
    # graph.add_conditional_edges("voice_to_text",lambda state: "exception_handler" if state.get("status") == "error" else "text_to_sql")
    # # graph.add_conditional_edges("voice_to_text",lambda state: "exception_handler" if state.get("status") == "error" else "text_to_sql")
    # graph.add_conditional_edges("text_to_sql",lambda state: "exception_handler" if state.get("status") == "error" else "execute_sql")
    # graph.add_conditional_edges("execute_sql",lambda state: "exception_handler" if state.get("status") == "error" else "generate_report")
    # graph.add_conditional_edges("generate_report",lambda state: "exception_handler" if state.get("status") == "error" else END)
    
    # graph.add_edge("exception_handler", END)


    # graph = StateGraph(QueryState)
    graph.add_node("fetch_details", fetch_details)
    graph.add_node("voice_to_text", voice_to_text)
    graph.add_node("translate_to_english", translate_to_english)
    # graph.add_node("check_completeness", question_completeness)
    graph.add_node("ask_missing_info", ask_missing_info)
    graph.add_node("text_to_sql", text_to_sql)
    graph.add_node("execute_sql", execute_sql)
    graph.add_node("translate_response", translate_response)

    # Edges
    graph.set_entry_point("fetch_details")
    graph.add_conditional_edges("fetch_details",  lambda state: "voice_to_text" if state.get("audio_path")  else "translate_to_english", 
                                {
                                    "voice_to_text": "voice_to_text",
                                    "translate_to_english": "translate_to_english"
                                })
    graph.add_edge("voice_to_text", "translate_to_english")
    graph.add_conditional_edges("translate_to_english",  lambda state: "translate_response" if state.get("audio_path")  else "ask_missing_info", 
                    {
                        "ask_missing_info": "ask_missing_info",
                        "translate_response": "translate_response"
                    }
                    )

    # Conditional branching based on completeness
    graph.add_conditional_edges(
        "ask_missing_info",
        lambda state: "text_to_sql" if state["is_complete"] == "complete"  else "translate_response",
        {
            "text_to_sql": "text_to_sql",
            "translate_response": "translate_response"
        }
    )
    # graph.add_edge("ask_missing_info", "voice_to_text")  # Loop back

    graph.add_edge("text_to_sql", "execute_sql")
    graph.add_edge("execute_sql", "translate_response")
    graph.add_edge("translate_response", END)
        

    workflow = graph.compile()
    return workflow