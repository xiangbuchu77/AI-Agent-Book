# 生成过程与推理参数

本节属于《Transformer》。

## Core Idea

LLM 输出是一步步生成的。每一步模型都会给出候选 token 的概率分布，再由采样策略决定最终选择。

temperature、top_p、max_tokens 等参数控制输出的随机性、覆盖范围和长度。生产系统通常需要更低随机性、更明确格式和更严格的停止条件。

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
- [Next](04-context-design.md)
