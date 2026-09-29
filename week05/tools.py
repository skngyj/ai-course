import ollama, json, datetime

def get_time():
    """지금 시각을 돌려준다"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def calc(expression: str):
    """수식 문자열을 계산한다. 예: '17 * 24'"""
    return str(eval(expression, {"__builtins__": {}}))

functions = {"get_time": get_time, "calc": calc}

messages = [{"role": "user", "content": "지금 몇 시야? 그리고 17 곱하기 24는?"}]
for step in range(5):
    r = ollama.chat(model="qwen3:8b", think=False, messages=messages, tools=[get_time, calc])
    messages.append(r.message)
    if not r.message.tool_calls:                    # 도구 호출이 없으면 최종 답
        print("답:", r.message.content)
        break
    for call in r.message.tool_calls:               # 모델이 요청한 도구를 실제로 실행
        name, args = call.function.name, call.function.arguments
        result = functions[name](**args)
        print(f"  도구 호출: {name}({args}) -> {result}")
        messages.append({"role": "tool", "content": result, "tool_name": name})