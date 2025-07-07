# backend-python-llm/agents/main_agent.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def main_agent(state):
    """
    Uses GPT to decide which tool(s) to invoke.
    Returns a list of tools to call based on user message.
    """
    user_input = state.input.get("message", "")
    memory = state.memory or ""

    prompt = f"""
You are a routing assistant.

Decide which of the following tools to use based on the user input:
1. get_volume_forecast → if user wants volume prediction.
2. get_market_events → if user is asking about market triggers.
3. explain_scenario → if user wants a human-style explanation or summary.

User said: "{user_input}"

Reply ONLY with the tool name(s) as a comma-separated list.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You help route user queries to the right agent."},
            {"role": "user", "content": prompt}
        ]
    )

    tool_names = [tool.strip() for tool in response.choices[0].message["content"].split(",")]

    return [{"tool": name, "input": state.input} for name in tool_names]
