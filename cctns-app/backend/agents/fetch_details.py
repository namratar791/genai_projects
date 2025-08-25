from states.CCTNSState import CCTNSState
from utils.logger import logger 


# audio_path = "cctns-app/backend/harvard.mp3"
def fetch_details( state: CCTNSState) :
    try:
        audio_path = state.get("audio_path", "")
        user_query = state.get("user_query", "")
        return {"status": "success", "audio_path": audio_path, "user_query": user_query}
    except:
        logger.info("99999........")
        return { "error": "error occurred in fetch_details", "status": "error"}