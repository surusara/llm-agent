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
            state_dict = state.dict() if hasattr(state, "dict") else dict(state)
            state_dict["output"] = response.choices[0].message["content"]
            return state_dict

        except Exception as e:
            state_dict = state.dict() if hasattr(state, "dict") else dict(state)
            state_dict["output"] = f"Error explaining: {str(e)}"
            return state_dict

    return ToolNode([explain])
    
