# Transformer 是什么：Attention、QKV 与生成机制

## Story Explanation

当用户问“帮我写一个客户邮件”时，模型不是从数据库里取出一封邮件，而是在已有上下文基础上一步步预测下一个 token。它看起来像在思考，其实是在大规模训练中学到的模式上进行条件生成。理解这一点，能让开发者更冷静地设计提示词和系统边界。

如果第 1 章说 AI 的本质是预测，那么 Transformer 就是现代大语言模型能做好预测的关键结构。它解决的核心问题很朴素：当模型看到一句话、一个问题或一段代码时，怎样知道哪些信息最相关？

Attention 可以先简单理解为“找最相关信息”。比如用户问“这份合同里付款条件是什么”，模型需要把注意力放在合同中的付款条款，而不是页眉、签名或无关说明。Transformer 的强大之处，就是它能在全局范围内建立这种相关性。

## Technical Explanation

Transformer 通过 attention 建模 token 之间的关系。Decoder-only LLM 按自回归方式生成输出：每一步根据前文和上下文计算候选 token 概率，再由采样策略选择结果。上下文设计、停止条件、temperature、top_p 和 max_tokens 都会影响最终行为。

Attention 的经典解释是 Q、K、V：

- Q = Query，表示当前位置想找什么信息。
- K = Key，表示每个位置能被匹配的特征。
- V = Value，表示真正要取出来参与计算的信息。

可以把它想象成查资料：Query 是你的问题，Key 是资料索引，Value 是资料内容。模型先用 Q 和 K 判断哪些位置相关，再从对应 V 中聚合信息。Self-Attention 则表示序列内部的 token 彼此查找相关信息。

Transformer 相比 RNN 的重要优势是全局注意力和并行计算。RNN 按顺序处理序列，长距离依赖容易衰减；Transformer 可以让远处 token 直接建立联系，因此更适合长文本、代码、对话和复杂上下文。

## Core Summary

- Attention = 找最相关信息。
- QKV = 查询、键、值。
- Transformer 解决了传统序列模型处理长依赖困难的问题。
- LLM 的生成过程是基于上下文逐 token 预测。

## Mermaid Diagram

```mermaid
flowchart LR
    N0["输入序列"]
    N1["Embedding"]
    N2["Attention"]
    N3["Decoder Blocks"]
    N4["概率分布"]
    N5["采样输出"]
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 -. feedback .-> N1
```

## Python Code

```python
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
```

See also: [example.py](example.py)

## Engineering Use Case

为代码生成工具设置较低随机性、明确停止符和输出格式，避免模型生成多余解释或未闭合代码块。

## Interview Questions

- Self-attention 解决了什么问题？
- 为什么 LLM 是逐 token 生成？
- 推理参数如何影响稳定性和创造性？
- Q、K、V 分别代表什么？
- 为什么 Transformer 比 RNN 更适合大语言模型？

## Quality Checklist

- 解释是否能被没有框架经验的开发者理解。
- 技术概念是否能落到输入、输出、状态、工具和评估。
- Mermaid 图是否表达了系统流向。
- Python 示例是否可独立运行。
- 工程案例是否说明真实业务价值。

## Navigation

- [Previous](../01-AI-Basics/index.md)
- [Next](../03-Prompt/index.md)
