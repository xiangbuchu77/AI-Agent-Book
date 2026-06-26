def call_weather_api(city):
    return {"city": city, "temperature": "18°C", "condition": "晴"}


def llm(user_input):
    return f"普通回答：{user_input}"


def function_call(user_input):
    if "天气" in user_input:
        tool_call = {"function": "get_weather", "arguments": {"city": "北京"}}
        result = call_weather_api(tool_call["arguments"]["city"])
        return f"{result['city']} 今天 {result['temperature']}，天气{result['condition']}"
    return llm(user_input)


print(function_call("查一下北京天气"))
