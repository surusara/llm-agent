from graph import build_graph
from memory_state import MemoryState

if __name__ == "__main__":
    graph = build_graph()

    #  Provide a valid input string to start the conversation
    user_query = "Will ECB and NFP affect FX volume this week?"

    #  Create MemoryState object with initial input
    state = MemoryState(input=user_query)

    #  Run the graph
    result = graph.invoke(state)

    #  Print final result
    print("\n=== Final Output ===")
    print(result.output)
   #this is new file
