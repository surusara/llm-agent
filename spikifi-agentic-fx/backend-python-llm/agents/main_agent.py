# backend-python-llm/agents/main_agent.py

import openai
import os
from langgraph.prebuilt import ParallelToolNode

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def create_main_agent():
    def route_tools(state):
        """
        Routes the user input to one or more tools based on LLM reasoning.
        Tools:
        - get_volume_forecast
        - get_market_events
        - explain_scenario
        """
        user_input = state.input.get("message", "")

        if not user_input:
            return []

        # Prompt to decide which tools to use
        decision_prompt = f"""
        Decide which of the following tools to use:
        1. get_volume_forecast → if user wants volume prediction.
        2. get_market_events → if user is asking about market triggers.
        3. explain_scenario → if user wants a summary explanation.

        User said: "{user_input}"

        Reply with a comma-separated list like: get_volume_forecast, explain_scenario
        """

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You help route user queries to the correct agent(s)."},
                    {"role": "user", "content": decision_prompt}
                ]
            )

            raw_output = completion.choices[0].message["content"]
            tool_names = [t.strip() for t in raw_output.split(",") if t.strip()]

            return [{"tool": t, "input": state.input} for t in tool_names]

        except Exception as e:
            return [{"tool": "explain_scenario", "input": {"message": f"Routing failed: {str(e)}"}}]

    return ParallelToolNode(route_tools)
