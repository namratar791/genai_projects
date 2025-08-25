import os
import sqlite3
from uuid import uuid4
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from graph.cctns_graph import run_cctns_agent
from db.database import setup_db
from IPython.display import Image, display
from states.CCTNSState import CCTNSState
# from utils.logger import logger
# import logging

# logging.basicConfig(
#     level=logging.INFO,  # minimum log level to capture (DEBUG, INFO, WARNING, ERROR)
#     format='%(asctime)s %(levelname)s %(name)s - %(message)s'
# )

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

memory_store = {}
setup_db()

@app.post("/process_audio/")
async def process_audio(request: Request, file: UploadFile):
    thread_id = request.headers.get("thread-id") or str(uuid4())
    filename = f"temp_{thread_id}.mp3"
    folder = "./"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    contents = await file.read()
    if not contents:
        raise ValueError("Uploaded file is empty")

    with open(path, "wb") as f:
        f.write(contents)

    print(f"Audio file saved at: {path}")

    state = CCTNSState(audio_path=path)
    # graph = build_graph()
    workflow = run_cctns_agent()
    final_state = workflow.invoke(state)
    print(final_state)
    # Store session memory
    memory_store[thread_id] = final_state

    os.remove(path)
    return {"thread_id": thread_id, "response": final_state}

@app.post("/process_text/")
async def process_text(request: Request):
    thread_id = request.headers.get("thread-id") or str(uuid4())

    data = await request.json()  # Get JSON body as a dict
    user_query = data.get("user_query", "")
    print(f"Audio file saved at: {user_query}")
    state = CCTNSState(user_query=user_query)
    # graph = build_graph()
    workflow = run_cctns_agent()
    final_state = workflow.invoke(state)
    print(final_state)
    # Store session memory
    memory_store[thread_id] = final_state

    return {"thread_id": thread_id, "response": final_state}


# if __name__ == "__main__":
#     # setup_db()
#     workflow = run_cctns_agent()
#     result_invoke = workflow.invoke({})
    # png_bytes = workflow.to_mermaid()
    # output_filename = "cctns-app/backend/graph_visualization.png"

    # Save the PNG bytes to a file
    # with open(output_filename, "wb") as f:
    #     f.write(png_bytes)

    # print(f"Graph visualization saved to {output_filename}")