from pydantic import BaseModel
from typing import Optional, Any

class MemoryState(BaseModel):
    input: dict  # e.g., {"message": "..."}
    memory: Optional[str] = ""
    output: Optional[Any] = None
