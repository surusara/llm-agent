import requests
import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.prebuilt import Tool, AgentExecutor
import uvicorn

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")

API_BASE_URL = os.getenv("ML_API_BASE_URL", "http://localhost:8000")

# -------------------------
# Tool 1: Predict FX Volume
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
# Tool 2: Macro Event Explanation (stub)
# -------------------------
def get_macro_event_tool(input):
    date = input.get("date", "2025-07-03")
    pair = input.get("fx_pair", "EUR/USD")
    return f"On {date}, ECB is expected to hike rates. This may impact {pair} trading volume."

# -------------------------
# Register tools
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
# LangGraph Agent
# -------------------------
def call_openai_chat(messages):
    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,
        messages=messages
    )
    return response['choices'][0]['message']['content']

agent_executor = AgentExecutor.from_tools(
    tools=tools,
    llm="gpt-4",  # Placeholder
    llm_func=call_openai_chat,
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
