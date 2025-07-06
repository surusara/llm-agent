import requests

def get_live_market_event(input_text: str) -> str:
    try:
        response = requests.post("http://backend-java:8080/live-market-event", json={"query": input_text})
        return response.json().get("response", "")
    except Exception as e:
        return f"Error fetching market event: {e}"