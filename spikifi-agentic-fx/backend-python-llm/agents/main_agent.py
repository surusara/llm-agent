# backend-python-llm/agents/main_agent.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def main_agent(state):
    """
    Routes user input to one or more tools:
    - get_volume_forecast
    - get_market_events
    - explain_scenario
    Returns a dict with tool_calls for LangGraph multi-tool pattern.
    """
    user_input = state.input.get("message", "")

    decision_prompt = f"""
You are a routing assistant.

Decide which of the following tools to use based on the user input:
1. get_volume_forecast → if user wants volume prediction.
2. get_market_events → if user is asking about market triggers.
3. explain_scenario → if user wants a human-style explanation.

User said: "{user_input}"

Reply ONLY with a comma-separated list of tool names.
"""

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You help route user queries to the right agent."},
            {"role": "user", "content": decision_prompt}
        ]
    )

    tool_names = [tool.strip() for tool in completion.choices[0].message["content"].split(",")]
    state_dict = state.dict() if hasattr(state, "dict") else dict(state)
    state_dict["tool_calls"] = [
        {"tool": name, "input": state.input}
        for name in tool_names
    ]
    return state_dict
