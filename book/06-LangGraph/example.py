def collect(state):
    state["data"] = [3, 7, 12]
    return state

def analyze(state):
    state["risk"] = max(state["data"]) > 10
    return state

def draft(state):
    state["message"] = "risk detected" if state["risk"] else "normal"
    return state

state = {}
for node in (collect, analyze, draft):
    state = node(state)
print(state)
