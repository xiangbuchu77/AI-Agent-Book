def estimate_tokens(text: str) -> int:
    # Rough English/Chinese mixed estimate for planning, not billing.
    return max(1, len(text) // 3)

def can_fit(system_prompt: str, user_input: str, limit: int = 8000) -> bool:
    return estimate_tokens(system_prompt) + estimate_tokens(user_input) < limit

print(can_fit("You are a careful assistant.", "summarize this document" * 200))
