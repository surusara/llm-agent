from langgraph.prebuilt import ToolNode

def create_main_agent():
    def agent_fn(state):
        """
        Main agent function that analyzes user input
        and delegates work to appropriate tools: 
        volume forecast and market event classification.
        """
        user_input = state.input

        return [
            {"tool": "get_volume_forecast", "input": user_input},
            {"tool": "get_market_events", "input": user_input}
        ]

    agent_fn.__name__ = "main_agent"
    agent_fn.__doc__ = "Routes user input to the volume forecast and market classification tools."

    return ToolNode(agent_fn)
