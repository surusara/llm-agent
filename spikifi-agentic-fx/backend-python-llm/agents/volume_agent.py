# backend-python-llm/agents/volume_agent.py

import requests
from langgraph.prebuilt import ToolNode

def create_volume_agent():
    def fetch_volume(state):
        """
        get_volume_forecast: Calls ML API to get FX volume forecast.
        """
        input_text = state.input.get("message", "")
        try:
            response = requests.post(
                "http://backend-python-ml:8500/predict",
                json={"message": input_text}
            )
            return [{"output": response.json()}]
        except Exception as e:
            return [{"output": f"Error fetching volume forecast: {str(e)}"}]

    return ToolNode([fetch_volume])
