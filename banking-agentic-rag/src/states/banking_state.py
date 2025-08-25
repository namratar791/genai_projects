




import uuid
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class SearchResult(BaseModel):
    source: str
    content: str
    status: str

class BankingState(BaseModel):
    user_query: str = Field(..., description="Latest query from the user")
    session: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique session ID")
    
    intents: List[str] = Field(default_factory=list, description="List of Intents")
    rag_results: Optional[SearchResult] = None
    db_results: Optional[SearchResult] = None
    web_results: Optional[SearchResult] = None

    # Short-term memory: last few interactions
    short_memory: List[str] = Field(default_factory=list, description="Rolling buffer of last few turns")
    
    # Long-term memory: summarized knowledge or embeddings persisted externally
    long_memory: Optional[str] = Field(None, description="Long-term summary or persistent knowledge")
    
    sentiment: str = Field(None , description="sentiment")
    action_taken: Optional[str] = Field(None, description="action taken")

    # Final response after processing
    status: str = Field(None , description="status")
    response: Optional[str] = Field(None, description="Agent/Graph response to user")
    