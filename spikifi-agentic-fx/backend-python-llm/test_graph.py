# backend-python-llm/test_graph.py

from graph import build_graph
from memory_state import MemoryState

def run_test():
    # Build the LangGraph instance
    graph = build_graph()

    # Simulate a user message
    user_query = {
        "message": "Will there be any FX volume spike tomorrow due to ECB announcement?"
    }

    # Initialize memory state
    initial_state = MemoryState(input=user_query)

    # Run the graph with the initial input
    print("Invoking graph with user input...")
    final_state = graph.invoke(initial_state)

    # Print final output
    print("\n=== Final Output ===")
    print(final_state.output)

    # Optional: Show entire state if needed
    print("\n=== Full Memory State ===")
    print(final_state)

if __name__ == "__main__":
    run_test()
