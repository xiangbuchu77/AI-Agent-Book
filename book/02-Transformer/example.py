import math


def softmax(scores):
    exp_scores = [math.exp(score) for score in scores]
    total = sum(exp_scores)
    return [score / total for score in exp_scores]


def attention(q, k, v):
    scores = [q * key for key in k]
    weights = softmax(scores)
    return sum(weight * value for weight, value in zip(weights, v))


query = 0.9
keys = [0.1, 0.8, 0.3]
values = [10, 50, 20]

print(attention(query, keys, values))
