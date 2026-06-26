def search_tool(query: str) -> str:
    return f"evidence for: {query}"

def agent(goal: str, max_steps: int = 3):
    state = {"goal": goal, "evidence": [], "done": False}
    for _ in range(max_steps):
        if not state["evidence"]:
            state["evidence"].append(search_tool(goal))
        else:
            state["done"] = True
            return state
    state["needs_human_review"] = True
    return state

print(agent("summarize project risk"))
