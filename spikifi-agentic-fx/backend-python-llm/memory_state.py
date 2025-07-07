from pydantic import BaseModel
from typing import Optional, Any, Dict

class MemoryState(BaseModel):
    input: Dict[str, Any]
    memory: Optional[str] = ""
    output: Optional[Any] = None
