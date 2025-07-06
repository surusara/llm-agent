from langgraph.prebuilt import ToolNode

def create_main_agent():
    def agent_fn(state):
        user_input = state.input  # assuming you’re using Pydantic MemoryState

        return [
            {"tool": "get_volume_forecast", "input": user_input},
            {"tool": "get_market_events", "input": user_input}
        ]

    return ToolNode(agent_fn)
