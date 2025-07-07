# backend-python-llm/test_graph.py

from graph import build_graph
from memory_state import MemoryState

if __name__ == "__main__":
    graph = build_graph()

    # Sample query
    user_query = {"message": "What is the FX volume forecast for tomorrow with ECB meeting?"}
    state = MemoryState(input=user_query)

    print("\n==== Invoking LangGraph ====")
    for step in graph.stream(state):
        print(f"\n>> Step: {step.key}")
        print(f"State: {step.value}")

    print("\n==== Final Output ====")
    final_state = graph.invoke(state)
    print(final_state)
