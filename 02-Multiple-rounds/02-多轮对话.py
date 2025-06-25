from importlib.resources import contents

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import getpass
import os
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'


load_dotenv()

# 初始化模型
model = ChatDeepSeek(
    model_name="deepseek-chat",
    temperature=0.5,
    max_tokens=1024
)

messages = [
    ("system","我是langchian学习助手"),
    ("human","我是学员xx"),
    ("system","你好"),
    ("human","你是谁，我是谁")
]
# 使用消息对象封装对话内容
messages = [
    SystemMessage(content="你是LangChain学习助手"),
    HumanMessage(content="你好"),
    AIMessage(content="你好！我是LangChain学习助手，请问你想了解什么？"),
    HumanMessage(content="LangChain有什么核心组件？")
]
print(model.invoke(messages).content)

