from states.CCTNSState import CCTNSState

def generate_report( state: CCTNSState) :
    try:
        rows = state.get("db_results","")
        if not rows:
            return "No records found."
        report = "CCTNS Report:\n"
        for row in rows:
            report += " | ".join(str(item) for item in row) + "\n"
        # return report
        print(f"Report: \n {report}")
        return {"status": "success", "report": report}
    except:
        return { "error": "error occurred in generate_report", "status": "error"}