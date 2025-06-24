# 📘 模块学习笔记：07-prompt封装

> 本笔记记录了对 LangChain 中“prompt 封装”模块的学习理解与代码实践，包括 PromptTemplate、ChatPromptTemplate、FewShotPromptTemplate 和外部加载 Prompt 等常用方式。
## 🧠 模块学习

---


### ✅ 简单 PromptTemplate

使用 `PromptTemplate.from_template` 构建一个基础的填空式提示：

```python
from langchain.prompts import PromptTemplate

simple_template = PromptTemplate.from_template("给我讲个关于{name}的笑话")
prompt = simple_template.format(name='xiaoA')
result = model.invoke(prompt).content

```
查看template与prompt，分别为
```aiignore
template: input_variables=['name'] input_types={} partial_variables={} template='给我讲个关于{name}的笑话'

prompt: 给我讲个关于xiaoA的笑话

result: 《职场新人类》  
小A第一天上班，领导让他复印文件。他认真研究了复印机半小时，最后郑重其事地把文件贴在玻璃窗上，用手机拍了张照，跑去文印室说："师傅，麻烦冲印一下，要高清的！"  

```
~~并不知道笑点在哪~~

---

## ✅ ChatPromptTemplate —— 多轮消息封装
### ChatPromptTemplate 用于构建多轮对话提示，支持系统、用户、AI 三种角色的历史消息嵌入，非常适合对话类模型调用。

```
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你是{product}应用"),
    HumanMessagePromptTemplate.from_template("你好"),
    AIMessagePromptTemplate.from_template("你好，我是{product}，请问您有什么需求呢？"),
    HumanMessagePromptTemplate.from_template("{query}")
])

prompt = template.format_messages(
    product="DeepSeek-Langchain学习助手",
    query="langchain的prompt该如何设计"
)

result = model.invoke(prompt).content
```
结果 prompt 是一个包含消息角色和内容的列表，可直接传入 model.invoke()：

```
template: input_variables=['product', 'query'] input_types={} partial_variables={} messages=[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=['product'], input_types={}, partial_variables={}, template='你是{product}应用'), additional_kwargs={}), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], input_types={}, partial_variables={}, template='你好'), additional_kwargs={}), AIMessagePromptTemplate(prompt=PromptTemplate(input_variables=['product'], input_types={}, partial_variables={}, template='你好，我是{product}，请问您有什么需求呢？'), additional_kwargs={}), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['query'], input_types={}, partial_variables={}, template='{query}'), additional_kwargs={})]

prompt: [SystemMessage(content='你是DeepSeek-Langchain学习助手应用', additional_kwargs={}, response_metadata={}), HumanMessage(content='你好', additional_kwargs={}, response_metadata={}), AIMessage(content='你好，我是DeepSeek-Langchain学习助手，请问您有什么需求呢？', additional_kwargs={}, response_metadata={}), HumanMessage(content='langchain的prompt该如何设计', additional_kwargs={}, response_metadata={})]

result: ...
```
### 🧠 prompt差异：多轮对话模型采用消息格式输入，而不是单纯的字符串 prompt。

---
## ✅ FewShotPromptTemplate —— 少样本提示
### FewShotPromptTemplate 允许在提示中提供多个“示例”来指导模型完成特定任务，适合翻译、分类、风格迁移等任务。

```
from langchain_core.prompts import  FewShotPromptTemplate
examples = [
    {"english": "Hello", "chinese": "你好"},
    {"english": "How are you?", "chinese": "你好吗？"},
    {"english": "What is your name?", "chinese": "你叫什么名字？"},
]

example_prompt = PromptTemplate(
    input_variables=["english", "chinese"],
    template="English: {english}\nChinese: {chinese}\n"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Translate the following English sentences to Chinese:",
    suffix="English: {input}\nChinese:",
    input_variables=["input"]
)

prompt = few_shot_prompt.format(input="Where is the library?")
result = model.invoke(prompt)
```
各变量结果
```aiignore
template: input_variables=['input'] input_types={} partial_variables={} examples=[{'english': 'Hello', 'chinese': '你好'}, {'english': 'How are you?', 'chinese': '你好吗？'}, {'english': 'What is your name?', 'chinese': '你叫什么名字？'}] example_prompt=PromptTemplate(input_variables=['chinese', 'english'], input_types={}, partial_variables={}, template='English: {english}\nChinese: {chinese}\n') suffix='English: {input}\nChinese:' prefix='Translate the following English sentences to Chinese:'

prompt: """Translate the following English sentences to Chinese:
Translate the following English sentences to Chinese:

English: Hello
Chinese: 你好


English: How are you?
Chinese: 你好吗？


English: What is your name?
Chinese: 你叫什么名字？


English: Where is the library?
Chinese:"""

result: 图书馆在哪里？
```

---
## ✅ 从外部文件加载 Prompt
### LangChain 支持从 .json、.yaml 等文件中加载 Prompt，实现配置与代码解耦。

#### 以json文件为例

json
```aiignore
{
  "_type": "prompt",
  "input_variables": [
    "company",
    "product"
  ],
  "template": "我是由{company}公司开发的{product}智能应用。"
}
```
加载方式
```aiignore
from langchain.prompts import load_prompt

template = load_prompt("prompt.json",encoding='utf-8')
prompt = template.format(company = "abalili", product = "dsspessk")
```
变量显示
```aiignore
template: input_variables=['company', 'product'] input_types={} partial_variables={} template='我是由{company}公司开发的{product}智能应用。'

prompt: 我是由abalili公司开发的dsspessk智能应用。
```
### 🧠 该方式由于其规范性、代码简洁性因而较为常用。

