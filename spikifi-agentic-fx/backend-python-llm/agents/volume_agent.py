# agents/volume_agent.py

import requests
from langgraph.prebuilt import ToolNode

def create_volume_agent():
    def fetch_volume(state):
        """
        get_volume_forecast: Predicts FX trade volume using ML.
        This tool calls the ML model API and returns a prediction based on the user's query.
        """
        input_text = state.input

        try:
            response = requests.post(
                "http://backend-python-ml:8500/predict",
                json={"query": input_text}
            )
            response_data = response.json()
            return [{"output": response_data}]
        except Exception as e:
            return [{"output": f"Error fetching volume forecast: {str(e)}"}]

    return ToolNode(fetch_volume)
