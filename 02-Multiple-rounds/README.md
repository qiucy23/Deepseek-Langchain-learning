# 📘 模块学习笔记：02-多轮对话

> 本笔记记录了对 LangChain 中“多轮对话”模块的学习理解与代码实践。

---

## 🧠 模块目标
### 实现多轮对话

- 简易写法
```aiignore
messages = [
    ("system","我是langchian学习助手"),
    ("human","我是学员xx"),
    ("system","你好"),
    ("human","你是谁，我是谁")
]
```
并不正规

- 标准写法
```aiignore
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 多轮消息，包括 AIMessage
messages = [
    SystemMessage(content="你是LangChain学习助手"),
    HumanMessage(content="你好"),
    AIMessage(content="你好！我是LangChain学习助手，请问你想了解什么？"),
    HumanMessage(content="LangChain有什么核心组件？")
]
```
使用SystemMessage, HumanMessage, AIMessage 定义系统指令, 人类回复以及AI回复。


## 💡细节反思

SystemMessage和AIMessage的区别为SystemMessage用于设定AI系统prompt指令，用于指导模型行为。