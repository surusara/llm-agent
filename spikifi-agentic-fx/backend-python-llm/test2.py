from langgraph.graph import StateGraph
from memory_state import MemoryState

from agents.main_agent import create_main_agent
from agents.volume_agent import create_volume_agent
from agents.market_agent import create_market_agent
from agents.explain_agent import create_explain_agent

# Define graph
builder = StateGraph(MemoryState)

# Add nodes
builder.add_node("main_agent", create_main_agent())
builder.add_node("get_volume_forecast", create_volume_agent())
builder.add_node("get_market_events", create_market_agent())
builder.add_node("explain_scenario", create_explain_agent())

# Set entry point and flow
builder.set_entry_point("main_agent")
builder.add_conditional_edges("main_agent", lambda x: x)

# Terminate each tool
builder.add_edge("get_volume_forecast", "__end__")
builder.add_edge("get_market_events", "__end__")
builder.add_edge("explain_scenario", "__end__")

# Compile graph
graph = builder.compile()

if __name__ == "__main__":
    test_input = MemoryState(input="Will FX volume spike due to ECB decision?")
    result = graph.invoke(test_input)
    print("\n--- Final Result ---")
    print(result.output)
