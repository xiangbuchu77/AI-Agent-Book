from dataclasses import dataclass

@dataclass
class Milestone:
    name: str
    outcome: str

path = [
    Milestone("LLM Basics", "understand tokens and context"),
    Milestone("RAG", "ground answers in documents"),
    Milestone("Agent", "combine tools, memory, and control"),
]

for step, milestone in enumerate(path, 1):
    print(f"{step}. {milestone.name}: {milestone.outcome}")
