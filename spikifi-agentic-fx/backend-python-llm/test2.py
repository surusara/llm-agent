from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from agents.volume_agent import create_volume_agent
from agents.market_agent import create_market_agent
from agents.explain_agent import create_explain_agent
from agents.main_agent import create_main_agent
from memory_state import MemoryState

# Create graph object using MemoryState
builder = StateGraph(MemoryState)

# Add nodes (tools + router)
builder.add_node("main_agent", create_main_agent())
builder.add_node("get_volume_forecast", create_volume_agent())
builder.add_node("get_market_events", create_market_agent())
builder.add_node("explain_scenario", create_explain_agent())

# Define routing logic
builder.set_entry_point("main_agent")

# Route to tools and back
builder.add_edge("main_agent", "get_volume_forecast")
builder.add_edge("main_agent", "get_market_events")
builder.add_edge("main_agent", "explain_scenario")

# End all tools after execution
builder.add_edge("get_volume_forecast", END := "__end__")
builder.add_edge("get_market_events", END)
builder.add_edge("explain_scenario", END)

# Build the graph
graph = builder.compile()

# Sample input
if __name__ == "__main__":
    test_input = MemoryState(input="Will FX volume spike due to the ECB rate hike?")
    result = graph.invoke(test_input)
    print("\n--- Final Output ---")
    print(result.output)
