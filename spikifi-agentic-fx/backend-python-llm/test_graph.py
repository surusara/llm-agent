# test_graph.py

from graph import build_graph
from memory_state import MemoryState

def run_test():
    # Step 1: Build the graph
    graph = build_graph()

    # Step 2: Create a mock user input (simulate chatbot message)
    user_input = input("Enter your message to the agent: ")
    state = MemoryState(input=user_input)

    # Step 3: Invoke the graph
    result = graph.invoke(state)

    # Step 4: Print results
    print("\n=== Agent Response ===")
    print("Output:", result.output)
    print("Memory:", result.memory)

if __name__ == "__main__":
    run_test()

