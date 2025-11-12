from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, ChatResponse, SourceDoc
from services.memory_service import get_or_create_session
from services.rag_graph import build_rag_graph
from config import CORS_ORIGINS

app = FastAPI(title="Azure LangGraph RAG Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_rag_graph()

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    state = get_or_create_session(req.user_id, req.thread_id)
    state.memory.chat_memory.add_user_message(req.query)

    new_state = graph.invoke(state)

    # Save response to memory
    state.memory.chat_memory.add_ai_message(new_state.last_answer)

    return ChatResponse(
        answer=new_state.last_answer,
        sources=[SourceDoc(**doc) for doc in new_state.context_docs]
    )
