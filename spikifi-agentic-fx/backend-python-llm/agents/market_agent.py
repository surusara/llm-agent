import openai
import requests
import os
from langgraph.prebuilt import ToolNode

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def create_market_agent():
    def fetch_market_events(state):
        """
        get_market_events: Fetches market events from Java backend and classifies them via GPT.
        """
        input_text = state.input

        try:
            response = requests.post(
                "http://backend-java:8080/live-market-event",
                json={"query": input_text}
            )
            raw_event_text = response.json().get("response", "")

            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an economic analyst who classifies market events."},
                    {"role": "user", "content": f"Classify this market event as one of: Scheduled Economic, Unscheduled Economic, Geopolitical.\n\nEvent: {raw_event_text}"}
                ]
            )

            classification = completion.choices[0].message["content"]

            return [{
                "output": {
                    "event": raw_event_text,
                    "classification": classification
                }
            }]
        except Exception as e:
            return [{"output": f"Error fetching/classifying market event: {str(e)}"}]

    return ToolNode([fetch_market_events])
