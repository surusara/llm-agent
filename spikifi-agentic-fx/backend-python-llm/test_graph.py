from graph import build_graph
from memory_state import MemoryState

def run_test():
    graph = build_graph()
    state = MemoryState(input="Will there be FX volatility this week due to NFP and MSCI rebalancing?")
    result = graph.invoke(state)
    print("\n=== Final Output ===")
    print(result.output)

if __name__ == "__main__":
    run_test()
