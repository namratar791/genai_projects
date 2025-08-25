import sqlite3
from states.CCTNSState import CCTNSState
from db.database import get_connection

def execute_sql( state: CCTNSState) :
    conn = sqlite3.connect("cctns.db")  # ✅ create fresh conn
    cursor = conn.cursor()
    status = None
    error_txt = None
    db_results = None 

    # print(f"state........{state}")
    sql_query = state.get("sql_query", "")
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        error_txt = None
        status = "success"
        db_results = rows
    except Exception as e:
        error_txt = f"SQL execution error: {e}"
        status = "error"
    finally:
        conn.close()
        return {"status": status, "error": error_txt, "db_results" : db_results}
    