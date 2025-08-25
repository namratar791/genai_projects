from typing import Literal, NotRequired, TypedDict


class CCTNSState(TypedDict, total=False):
    user_query: str
    sql_query: str
    db_results: list
    report: str
    error: str
    status: Literal["success", "error"]
    is_complete: NotRequired[str]
    query_type: Literal["relevant_complete", "irrelevant", "relevant_incomplete"]
    translated_text: str
    selected_language : NotRequired[str]
    next_prompt : NotRequired[str]
    final_response : NotRequired[str]
    audio_path: str