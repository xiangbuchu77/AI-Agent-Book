from string import Template

prompt_template = Template("""
你是：$role

任务：$task

背景信息：
$context

要求：
- $constraint_1
- $constraint_2

输出格式：
$output_format

如果信息不足，请回答：无法根据现有信息确认。
""")

prompt = prompt_template.substitute(
    role="资深 AI 工程师",
    task="解释 Transformer",
    context="读者是零基础开发者",
    constraint_1="不要使用复杂公式",
    constraint_2="使用生活类比",
    output_format="分点输出：核心概念、简单例子、为什么重要",
)

print(prompt)
