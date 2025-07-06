from fastapi import FastAPI, Request
from graph import build_graph
from memory_store import get_memory, update_memory

app = FastAPI()
graph = build_graph()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    session_id = data.get("session_id", "default")

    memory = get_memory(session_id)
    update_memory(session_id, f"User: {user_input}")

    result = graph.invoke({
        "input": user_input,
        "memory": "\n".join(memory)
    })

    response = result.get("output", "Sorry, I couldn't process that.")
    update_memory(session_id, f"Bot: {response}")

    return {"response": response}