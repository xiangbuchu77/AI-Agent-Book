from math import sqrt

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(v):
    return sqrt(sum(x * x for x in v))

def cosine(a, b):
    return dot(a, b) / (norm(a) * norm(b) or 1)

docs = {"policy": [0.9, 0.1], "pricing": [0.2, 0.8]}
query = [0.8, 0.2]
print(max(docs, key=lambda name: cosine(query, docs[name])))
