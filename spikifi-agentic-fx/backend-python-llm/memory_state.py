class MemoryState(BaseModel):
    input: str
    memory: Optional[str] = ""
    output: Optional[Any] = None
