import os
from langgraph.prebuilt import ToolNode
from openai import OpenAI

# Setup OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),        # Optional for Azure/OpenAI enterprise setups
    organization=os.getenv("OPENAI_ORG")          # Optional
)

def create_explain_agent():
    def explain(state):
        """
        explain_scenario: Uses LLM to explain the FX volume outlook and its market implications.
        This tool interprets the volume forecast and market conditions to generate a human-readable summary.
        """
        input_text = state.input

        try:
            prompt = f"Explain the FX volume outlook and market impact based on this: {input_text}"
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial analyst who explains complex data to traders."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            return [{"output": result}]
        except Exception as e:
            return [{"output": f"Error explaining scenario: {str(e)}"}]

    return ToolNode([explain])
