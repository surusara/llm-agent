# backend-python-llm/api.py

from fastapi import FastAPI, Request
from memory_state import MemoryState
from graph import build_graph
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")
    state = MemoryState(input={"message": message})
    result = graph.invoke(state)
    return {"result": result.output}
