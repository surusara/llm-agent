# backend-python-llm/agents/market_agent.py

import requests
import openai
import os
from langgraph.prebuilt import ToolNode

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def create_market_agent():
    def fetch_market_events(state):
        """
        get_market_events: Fetches live market events and classifies them.
        """
        input_text = state.input.get("message", "")

        try:
            response = requests.post(
                "http://backend-java:8080/live-market-event",
                json={"message": input_text}
            )
            raw_event = response.json().get("response", "")

            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You classify market events."},
                    {"role": "user", "content": f"Classify: {raw_event} into Scheduled, Unscheduled or Geopolitical."}
                ]
            )
            classification = completion.choices[0].message["content"]
            return [{"output": {"event": raw_event, "classification": classification}}]

        except Exception as e:
            return [{"output": f"Error: {str(e)}"}]

    return ToolNode([fetch_market_events])
