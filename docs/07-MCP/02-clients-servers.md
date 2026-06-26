# Host、Client 与 Server

本节属于《MCP》。

## Core Idea

在 MCP 架构中，用户面对的是 Host，Host 内部通过 Client 与一个或多个 MCP Server 通信。Server 暴露工具、资源和提示模板。

这种分层让能力提供方和 AI 应用方解耦。开发者可以独立开发 MCP Server，再被不同支持 MCP 的客户端复用。

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
- [Next](03-tools-resources-prompts.md)
