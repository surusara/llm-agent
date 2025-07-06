import openai
import os
from langgraph.prebuilt import ToolNode

openai.api_key = os.getenv("OPENAI_API_KEY")

def create_explain_agent():
    def explain(input_text):
        prompt = f"Explain the FX volume outlook and market impact based on this: {input_text}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analyst who explains complex data to traders."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"]

    return ToolNode(explain)
