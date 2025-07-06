import requests
from langgraph.prebuilt import ToolNode

def create_volume_agent():
    def fetch_volume(input_text):
        try:
            response = requests.post("http://backend-ml:8500/predict", json={"query": input_text})
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    return ToolNode(fetch_volume)
