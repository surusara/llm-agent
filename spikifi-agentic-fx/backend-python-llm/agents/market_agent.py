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
        get_market_events: Fetches market events from backend and classifies them via LLM.
        """
        input_text = state.input.get("query", "")
        try:
            response = requests.post(
                "http://backend-java:8080/live-market-event",
                json={"query": input_text}
            )
            raw_event_text = response.json().get("response", "")

            classification_prompt = f"""
Classify the following market event into one of:
- Scheduled Economic Event
- Unscheduled Economic Event
- Geopolitical Event

Event: {raw_event_text}

Also explain the rationale behind the classification.
"""

            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an economic analyst."},
                    {"role": "user", "content": classification_prompt}
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
            return [{"output": f"Error fetching/classifying event: {str(e)}"}]

    return ToolNode([fetch_market_events])
