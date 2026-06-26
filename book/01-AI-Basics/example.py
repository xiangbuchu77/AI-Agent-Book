from collections import Counter

history = [
    "AI is prediction",
    "AI is pattern matching",
    "AI is prediction",
    "LLM predicts the next token",
    "AI is probability",
]

words = []
for sentence in history:
    words.extend(sentence.lower().split())

counter = Counter(words)

print("Most common patterns:")
for word, count in counter.most_common(5):
    print(word, count)
