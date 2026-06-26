from datetime import datetime
import json

def log_event(step, model, cost, status):
    event = {
        "time": datetime.utcnow().isoformat(),
        "step": step,
        "model": model,
        "cost_usd": cost,
        "status": status,
    }
    print(json.dumps(event, ensure_ascii=False))

log_event("tool_call", "gpt-class", 0.002, "success")
