import os
import openai
from langgraph.prebuilt import ToolNode

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def create_explain_agent():
    def explain(state):
        """
        explain_scenario: Uses GPT to explain FX volume outlook and market impact.
        """
        input_text = state.input.get("message", "")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial analyst who explains complex data to traders."},
                    {"role": "user", "content": f"Explain the FX volume outlook and market impact based on this: {input_text}"}
                ]
            )

            return [{"output": response.choices[0].message["content"]}]
        except Exception as e:
            return [{"output": f"Error explaining scenario: {str(e)}"}]

    return ToolNode([explain])
