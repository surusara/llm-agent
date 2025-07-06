# backend-python-llm/agents/main_agent.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def create_main_agent():
    def main_agent(state):
        """
        Uses GPT to decide which tool(s) to invoke.
        Returns a list of tools to call.
        """
        user_input = state.input
        memory = state.memory or ""

        decision_prompt = f"""
You are a routing assistant.

Decide which of the following tools to use based on the user input:
1. get_volume_forecast → if user wants volume prediction.
2. get_market_events → if user is asking about market triggers.
3. explain_scenario → if user wants human-style explanation or summary.

User said: "{user_input}"

Reply ONLY with the tool name(s) as a comma-separated list (e.g. "get_volume_forecast, explain_scenario")
"""

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You help route user queries to the right agent."},
                {"role": "user", "content": decision_prompt}
            ]
        )

        tool_list = completion.choices[0].message["content"]
        tool_names = [tool.strip() for tool in tool_list.split(",")]

        # Build tool invocations for LangGraph
        return [{"tool": tool, "input": user_input} for tool in tool_names]

    return main_agent
