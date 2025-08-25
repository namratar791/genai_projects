import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from states.CCTNSState import CCTNSState
from openai import OpenAI  # New official client from latest openai python SDK
from utils.logger import logger 

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
# audio_path = "cctns-app/backend/harvard.mp3"
def voice_to_text( state: CCTNSState) :
    try:
        audio_path = state.get("audio_path", "")
        # if not os.path.isfile(audio_path):
        #     print("Audio file not found:")
        #     raise FileNotFoundError(f" Audio file not found: {audio_path}")

        with open(audio_path, "rb") as f:
            resp = client.audio.transcriptions.create(
                file=f,
                model="whisper-1"
            )
            resp_dict = resp.dict()
            transcribed_text = resp_dict.get("text", "")
            logger.info(f"*******:{resp_dict}")

        return {"status": "success", "user_query": transcribed_text}
    except:
        logger.info("error...*****")
        return { "error": "error occurred in voice_to_text", "status": "error"}