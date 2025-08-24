from pickle import LIST
from pyexpat import model
from openai import OpenAI
import json

from inspect import signature

# 配置客户端指向本地Ollama服务
client = OpenAI(
    base_url="http://localhost:11434/v1",  # 注意/v1后缀
    api_key="ollama"  # 任意非空字符串即可
)


# openai client 调用function call tools


# 生成embedding
response = client.embeddings.create(
    model="nomic-embed-text:latest",
    input="The quick brown fox jumps over the lazy dog",

    encoding_format="float"  # 可选，默认就是float
)

# 获取embedding向量
embedding = response.data[0].embedding
print(f"Embedding维度: {len(embedding)}")
print(f"前5个值: {embedding[:5]}")




# function calls test
def get_current_weather(location, unit="celsius"):
    """
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "模拟天气API调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["location"]
            }
        }
    }
    """
    print(f"正在获取 {location} 的天气（单位: {unit}）")
    return json.dumps({
        "location": location,
        "temperature": "22",
        "unit": unit,
        "forecast": ["晴朗"]
    })

def send_email(recipient:str, subject:str, body:str) ->json:
    """{
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {
                        "type": "string",
                        "description": "收件人邮箱"
                    },
                    "subject": {
                        "type": "string",
                        "description": "邮件主题"
                    },
                    "body": {
                        "type": "string",
                        "description": "邮件内容"
                    }
                },
                "required": ["recipient"]
            }
        }
}
    """
    print(f"发送邮件给 {recipient}，主题: {subject}")
    print(f"内容: {body}")
    return json.dumps({"status": "success", "message": "邮件已发送"})

sig = signature(send_email)
print("send_email signature: ",sig)
print("Parameters:  ",sig.parameters)
print("Return annotation:  ",sig.return_annotation)
def gen_tools_desc(funcs):
    from inspect import signature
    res = []
    for func in funcs:
        func_desc = func.__doc__
        # sig = signature(func)
        # print("func signature: ",sig)
        # print("Parameters:  ",sig.parameters['recipient'])
        # print("sig.parameters['recipient']: ", type(sig.parameters['recipient']))
        # print("Return annotation:  ",sig.return_annotation)
        # template = template.format(func.__name__, func.__doc__, sig.parameters['recipient'])
        print(func_desc)
        res.append(json.loads(func_desc))
    return res


print("gen_tools_desc: ", gen_tools_desc([send_email, get_current_weather]))

tools_func= {
    "get_current_weather": get_current_weather,
    "send_email": send_email
}


tools_desc = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如'北京'或'New York'",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位",
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送电子邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["recipient", "subject", "body"]
            }
        }
    }
]


tools_dict = {'tools_func': tools_func, 'tools_desc': tools_desc}

from typing import List, Dict

def chat_with_tools(prompt: str, messages: List[Dict], tools: List[Dict], model_name: str="qwen2.5:7b"):
    """
    与LLM对话并处理工具调用
    
    :param messages: 对话历史消息
    :param tools: 可用工具列表
    :return: 最终响应内容
    """
    # 第一步：获取LLM初始响应
    response = client.chat.completions.create(
        model=model_name,  # 或 gpt-4-turbo
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]+messages,
        tools=tools['tools_desc'],
        tool_choice="auto",  # 让模型决定是否调用工具
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # 如果没有工具调用，直接返回响应
    if not tool_calls:
        return response_message.content
    
    # 第二步：处理工具调用
    messages.append(response_message)  # 将LLM的响应添加到对话历史
    
    # 执行所有工具调用
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # 调用对应的工具函数
        if function_name in tools_dict['tools_func']:
            function_response = tools_dict['tools_func'][function_name](**function_args)
        else:
            function_response = {"error": f"未知工具: {function_name}"}
        
        # 将工具响应添加到对话历史
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(function_response),
        })
    
    # 第三步：将工具结果发送给LLM进行总结
    second_response = client.chat.completions.create(
        model=model_name,
        messages=messages,
    )
    
    return second_response.choices[0].message.content

prompt = """
请严格下面要求回答，不得添加虚构信息：
要求：
1. 如果有可以适合的tool call,必须包含tool call返回的信息 且确保真实
2. 禁止添加任何数据中不存在的信息
"""
resp = chat_with_tools(prompt, [
    {
        "role": "user",
        "content": "我想知道北京的天气。请以celsius单位返回结果给我， 并给一些旅游建议"
    }
], tools_dict, "qwen2.5:7b")

print("LLM resp:", resp)