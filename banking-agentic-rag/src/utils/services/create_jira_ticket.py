import requests
from utils.app_config import JIRA_URL, JIRA_USER, JIRA_TOKEN, JIRA_PROJECT



def create_jira_ticket(question: str):
    try:
        url = f"{JIRA_URL}/rest/api/3/issue"
        headers = {
            "Content-Type": "application/json"
        }
        print("jira")
        auth = (JIRA_USER, JIRA_TOKEN)
        payload = {
            "fields": {
                "project": {"key": JIRA_PROJECT},
                "summary": f"Ticket escalation : {question[:50]}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                        "type": "paragraph",
                        "content": [
                            {
                            "text":  f"Original Question: {question}",
                            "type": "text"
                            }
                        ]
                        }
                    ]
                },
                "issuetype": {"name": "Task"}
            }
        }
        # requests.post(url, json=payload, headers=headers, auth=auth)
        response = requests.post(url, json=payload, headers=headers, auth=auth)

        # ✅ check response
        if response.status_code == 201:  # JIRA returns 201 Created on success
            data = response.json()
            return {
                "status": "success",
                "ticket_id": data.get("key"),
                "url": f"{JIRA_URL}/browse/{data.get('key')}"
            }
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "response": response.text
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    