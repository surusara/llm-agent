import requests
from langgraph.prebuilt import Tool, AgentExecutor
from langgraph.graph import StateGraph
import openai
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

# -------------------------
# Configuration
# -------------------------
openai.api_key = "<YOUR_OPENAI_API_KEY>"
API_BASE_URL = "http://localhost:8000"  # Update with actual FastAPI endpoint

# -------------------------
# Tool: Predict FX Volume
# -------------------------
def predict_volume_tool(input):
    payload = {
        "fx_pair": input.get("fx_pair", "EUR/USD"),
        "volatility": input.get("volatility", 0.6),
        "fx_rate": input.get("fx_rate", 1.08),
        "macro_event_flag": input.get("macro_event_flag", 1)
    }
    response = requests.post(f"{API_BASE_URL}/predict", json=payload)
    return f"Predicted FX volume is {response.json().get('predicted_volume')}"

# -------------------------
# Tool: Get Macro Event Insight
# -------------------------
def get_macro_event_tool(input):
    date = input.get("date", "2025-07-03")
    pair = input.get("fx_pair", "EUR/USD")
    return f"On {date}, ECB is expected to hike rates. This may impact {pair} trading volume."

# -------------------------
# Register Tools
# -------------------------
tools = [
    Tool(
        name="predict_fx_volume",
        description="Predicts FX volume for a given FX pair and market conditions",
        func=predict_volume_tool
    ),
    Tool(
        name="get_macro_event",
        description="Provides macro event impact explanation for FX pair",
        func=get_macro_event_tool
    )
]

# -------------------------
# Define LangGraph Agent
# -------------------------
agent_executor = AgentExecutor.from_tools(
    tools=tools,
    llm="gpt-4",
    system_prompt="""
    You are an intelligent FX trading assistant.
    Your job is to:
    - Predict volume for currency pairs based on user inputs
    - Explain macro event impacts on FX volume
    - Use tools if needed to retrieve data
    - Respond in clear, trader-friendly language.
    """
)

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    result = agent_executor.invoke(req.message)
    return {"reply": result["output"]}

# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
