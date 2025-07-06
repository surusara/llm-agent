from langgraph.prebuilt import ToolNode

def create_main_agent():
    def agent_fn(state):
        user_input = state.get("input", "")
        memory = state.get("memory", "")

        return {
            "actions": [
                {"tool": "get_volume_forecast", "input": user_input},
                {"tool": "get_market_events", "input": user_input}
            ],
            "state": state
        }

    return ToolNode(agent_fn)