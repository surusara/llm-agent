from pydantic import BaseModel
from typing import Optional, Any

class MemoryState(BaseModel):
    input: str
    memory: Optional[str] = ""
    output: Optional[Any] = None
    
