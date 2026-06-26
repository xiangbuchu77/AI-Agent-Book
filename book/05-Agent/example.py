def llm(user_input):
    if "天气" in user_input:
        return {"need_tool": True, "tool": "weather", "args": {"city": "北京"}}
    return {"need_tool": False, "answer": "直接回答用户问题"}


def weather_tool(city):
    return f"{city} 今天 18°C"


def agent(user_input):
    thought = llm(user_input)
    if thought["need_tool"]:
        result = weather_tool(thought["args"]["city"])
        return f"工具结果：{result}。最终回答：北京今天 18°C。"
    return thought["answer"]


print(agent("查一下北京天气"))
