import openai
import os
from langgraph.prebuilt import ToolNode

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def create_main_agent():
    def main_agent(state):
        """
        main_agent: Routes user input to one or more of:
        - get_volume_forecast
        - get_market_events
        - explain_scenario
        """
        user_input = state.input.get("query", "")
        memory = state.memory or ""

        prompt = f"""
You are a routing assistant.

Choose tools based on input:
- get_volume_forecast → volume prediction
- get_market_events → market events
- explain_scenario → natural language explanation

User said: "{user_input}"
Reply with comma-separated tool names only.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You help decide which tool(s) to call."},
                {"role": "user", "content": prompt}
            ]
        )
        tool_list = response.choices[0].message["content"]
        tools = [tool.strip() for tool in tool_list.split(",")]

        # Output tool call instruction(s)
        return [{"tool": tool, "input": state.input} for tool in tools]

    return ToolNode([main_agent])
