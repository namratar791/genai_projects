from states.CCTNSState import CCTNSState



def question_completeness(state: CCTNSState):
    try:
        return {"status": "success", "error": None, "is_complete": "True"}
    except:
        return { "error": "error occurred in generate_report", "status": "error", "is_complete": None}