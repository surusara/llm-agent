import requests
from langgraph.prebuilt import ToolNode
import openai
import os

# Load OpenAI credentials from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.organization = os.getenv("OPENAI_ORG")

def create_market_agent():
    def fetch_market_events(state):
        """
        get_market_events: Fetches market events and classifies them using an LLM.
        Calls an external API to get the raw market event description,
        then uses GPT to classify it as a Scheduled Economic, Unscheduled Economic, or Geopolitical Event.
        """
        input_text = state.input

        try:
            # Step 1: Fetch raw market event description from another service
            response = requests.post("http://backend-java:8080/live-market-event", json={"query": input_text})
            raw_event_text = response.json().get("response", "")

            # Step 2: Use LLM to categorize the event
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an economic analyst who classifies market events."},
                    {"role": "user", "content": f"""Classify the following market event into one of these categories:
                    - Scheduled Economic Event
                    - Unscheduled Economic Event
                    - Geopolitical Event
                    
Event: {raw_event_text}

Also provide a short explanation."""}
                ]
            )

            classification_result = completion.choices[0].message["content"]

            return [{
                "output": {
                    "raw_event": raw_event_text,
                    "classification": classification_result
                }
            }]

        except Exception as e:
            return [{"output": f"Error fetching or classifying market event: {str(e)}"}]

    return ToolNode([fetch_market_events])
