# Token 与 Embedding

本节属于《AI 基础》。

## Core Idea

LLM 处理的基本单位通常是 token。文本会先被切分成 token，再映射为向量表示，模型通过这些向量学习语义、语法和上下文关系。

Embedding 让文本可以被比较、聚类和检索。RAG 系统中的向量检索，本质上就是利用 embedding 把自然语言问题映射到可计算的语义空间。

## Engineering Notes

在工程实践中，最重要的是把概念转化为可执行的边界：输入是什么，输出是什么，失败时如何处理，如何观测质量，如何回滚错误。

如果一个能力无法被测试、无法被记录、无法被复现，它就不应该直接进入生产级 Agent 的关键路径。

## Common Pitfalls

- 把模型输出当成确定性事实。
- 用更长的 Prompt 掩盖系统边界不清。
- 在没有评估集的情况下反复调参。
- 忽略权限、成本、延迟和失败恢复。

## Practical Checklist

- 明确本节概念在真实 Agent 系统中的位置。
- 区分模型能力、工程约束和业务规则。
- 为后续代码示例保留可测试、可评估的接口。

## Next Step

本节是 v0.1 草稿，后续会补充代码示例、架构图、案例和练习。

## Navigation

- [Back to Chapter Index](index.md)
- [Next](03-training-inference.md)
