# backend-python-llm/graph.py

from langgraph.graph import StateGraph
from agents.main_agent import create_main_agent
from agents.volume_agent import create_volume_agent
from agents.market_agent import create_market_agent
from agents.explain_agent import create_explain_agent
from memory_state import MemoryState

def build_graph():
    # Initialize the graph with state schema
    builder = StateGraph(MemoryState)

    # Add all agent nodes
    builder.add_node("main", create_main_agent())  # ParallelToolNode
    builder.add_node("get_volume_forecast", create_volume_agent())
    builder.add_node("get_market_events", create_market_agent())
    builder.add_node("explain_scenario", create_explain_agent())

    # Set the entry point
    builder.set_entry_point("main")

    # Set edges from main agent to tools
    builder.add_edge("main", "get_volume_forecast")
    builder.add_edge("main", "get_market_events")
    builder.add_edge("main", "explain_scenario")

    # After each tool completes, route output back to main for further input
    builder.add_edge("get_volume_forecast", "main")
    builder.add_edge("get_market_events", "main")
    builder.add_edge("explain_scenario", "main")

    # Compile the graph
    return builder.compile()
