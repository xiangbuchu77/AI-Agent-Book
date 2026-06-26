from string import Template

prompt = Template("""
Role: $role
Task: $task
Context: $context
Constraints: return JSON with keys: summary, risk, next_action.
""")

print(prompt.substitute(
    role="senior AI product analyst",
    task="analyze customer feedback",
    context="Users report slow onboarding."
))
