import random

def sample_next(candidates, temperature=0.7):
    adjusted = [(token, score / max(temperature, 0.01)) for token, score in candidates]
    total = sum(score for _, score in adjusted)
    pick = random.random() * total
    upto = 0
    for token, score in adjusted:
        upto += score
        if upto >= pick:
            return token

print(sample_next([("safe", 0.7), ("creative", 0.2), ("wild", 0.1)]))
