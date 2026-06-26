state = {}


def planner_node(state):
    state["plan"] = "search data -> analyze -> write report"
    return state


def tool_node(state):
    state["data"] = "sales increased, conversion dropped"
    return state


def writer_node(state):
    state["report"] = f"Plan: {state['plan']} | Data: {state['data']}"
    return state


for node in (planner_node, tool_node, writer_node):
    state = node(state)

print(state["report"])
