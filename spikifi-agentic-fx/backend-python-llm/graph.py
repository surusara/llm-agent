from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import Optional, Any

from agents.main_agent import create_main_agent
from agents.volume_agent import create_volume_agent
from agents.market_agent import create_market_agent

class MemoryState(BaseModel):
    input: str
    memory: Optional[str] = ""
    output: Optional[Any] = None

def build_graph():
    builder = StateGraph(MemoryState)

    builder.add_node("main", create_main_agent())
    builder.add_node("get_volume_forecast", create_volume_agent())
    builder.add_node("get_market_events", create_market_agent())

    builder.set_entry_point("main")

    builder.add_edge("main", "get_volume_forecast")
    builder.add_edge("main", "get_market_events")
    builder.add_edge("get_volume_forecast", "main")
    builder.add_edge("get_market_events", "main")

    return builder.compile()
