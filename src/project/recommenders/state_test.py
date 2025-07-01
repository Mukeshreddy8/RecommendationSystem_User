# 📁 src/project/recommenders/state_test.py

from src.project.recommenders.State import build_graph

if __name__ == "__main__":
    graph = build_graph()

    state = {"user": "Theresa Lowe"}
    result = graph.invoke(state)

    print("\n✅ FINAL OUTPUT:\n")
    print(result["combine_result"])
