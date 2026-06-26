from pathlib import Path

folders = ["app", "prompts", "tools", "retrieval", "evals", "logs"]
for folder in folders:
    Path(folder).mkdir(exist_ok=True)
print("project skeleton ready")
