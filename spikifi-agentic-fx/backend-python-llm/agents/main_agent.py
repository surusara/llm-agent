import openai
import os
from langgraph.prebuilt import ToolNode

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def create_main_agent():
    def main_agent(state):
        """
        Routes the user input to the appropriate tool(s):
        - get_volume_forecast
        - get_market_events
        - explain_scenario
        """
        user_input = state.input
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

        tools = [tool.strip() for tool in response.choices[0].message["content"].split(",")]
        return [{"tool": tool, "input": user_input} for tool in tools]

    return ToolNode([main_agent])
