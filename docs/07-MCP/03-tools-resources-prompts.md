# Tools、Resources 与 Prompts

本节属于《MCP》。

## Core Idea

Tools 用于执行动作，Resources 用于暴露可读取的上下文，Prompts 用于提供可复用的任务模板。三者对应 Agent 系统中的行动、知识和指令。

设计 MCP Server 时，要清楚每个能力属于哪一类。能读取的不一定能执行，能执行的必须有更严格的权限和审计。

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
- [Next](04-security.md)
