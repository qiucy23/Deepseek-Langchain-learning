from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'


load_dotenv()

# 初始化模型
model = ChatDeepSeek(
    model_name="deepseek-chat",
    temperature=0.5,
    max_tokens=1024,
    api_key = "my-api-key",
)

print(model.invoke("你是谁").content)
