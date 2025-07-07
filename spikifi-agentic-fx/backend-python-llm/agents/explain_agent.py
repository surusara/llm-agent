# backend-python-llm/agents/explain_agent.py

import openai
import os
from langgraph.prebuilt import ToolNode

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def create_explain_agent():
    def explain(state):
        """
        explain_scenario: Explains FX volume and market impact.
        """
        input_text = state.input.get("message", "")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial analyst."},
                    {"role": "user", "content": f"Explain FX impact for: {input_text}"}
                ]
            )
            return [{"output": response.choices[0].message["content"]}]

        except Exception as e:
            return [{"output": f"Error explaining: {str(e)}"}]

    return ToolNode([explain])
