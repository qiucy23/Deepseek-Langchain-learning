from dataclasses import Field
from importlib.resources import contents

from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.output_parsers import CommaSeparatedListOutputParser, PydanticOutputParser
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import getpass
import os
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, \
    AIMessagePromptTemplate, FewShotPromptTemplate
from langchain.prompts import PromptTemplate
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

load_dotenv()

class Writer(BaseModel):
    name: str = Field(description = '作家名字')
    nationality: str = Field(description = "作家国籍")
    dbz : list[str] = Field(description = "作家的代表作")
# 初始化模型
model = ChatDeepSeek(
    model_name="deepseek-chat",
    temperature=0.5,
    max_tokens=1024
)
# Prompttemplate
simple_template = PromptTemplate.from_template("给我讲个关于{name}的笑话")

print(simple_template)
print(simple_template.format(name = 'xiaoA'))
print(model.invoke(simple_template.format(name = 'xiaoA')).content)
# ChatPromptTemplate
template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("你是{product}应用"),
        HumanMessagePromptTemplate.from_template("你好"),
        AIMessagePromptTemplate.from_template("你好，我是{product}，请问您有什么需求呢？"),
        HumanMessagePromptTemplate.from_template("{query}")
    ]
)
prompt = template.format_messages(
    product = "DeepSeek-Langchain学习助手",
    name = "xiaoA",
    query = "langchain和deepseek的关系是什么？"
)
print(template)
print(prompt)
result = model.invoke(prompt)
content = result.content
print(content)
# FewShotPromptTemplate
# 预先设计例子-直接翻译器
examples = [
    {"english": "Hello", "chinese": "你好"},
    {"english": "How are you?", "chinese": "你好吗？"},
    {"english": "What is your name?", "chinese": "你叫什么名字？"},
]
# 定义示例格式模板
example_prompt = PromptTemplate(
    input_variables=["english", "chinese"],
    template="English: {english}\nChinese: {chinese}\n"
)

# FewShotPromptTemplate 构建
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Translate the following English sentences to Chinese:",
    suffix="English: {input}\nChinese:",
    input_variables=["input"]
)

print(few_shot_prompt)
prompt = few_shot_prompt.format(input="Where is the library?")
print(prompt)
result = model.invoke(prompt)
print(result.content)


# 从文档加载
from langchain.prompts import load_prompt

template = load_prompt("prompt.json",encoding='utf-8')
prompt = template.format(company = "abalili", product = "dsspessk")
print(template)
print(prompt)
