import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI


os.environ["http_proxy"] = "http://127.0.0.1:33210"
os.environ["https_proxy"] = "http://127.0.0.1:33210"

API_KEY = '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'

from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

if __name__ == '__main__':
    # llm = OpenAI(max_tokens=1024, openai_api_key=API_KEY)
    # print(llm.predict("请你介绍“中文”"))
    chat = ChatAnthropic()

    # steaming
    llm = ChatOpenAI(streaming=True, max_tokens=2048,
                     openai_api_key='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')

    # prompt = ChatPromptTemplate.from_messages(
    #     [("system", "你是一个专业的AI助手。"), ("human", "{query}")]
    # )

    # llm_chain = prompt | llm

    ret = llm.stream("你好")
    for token in ret:
        print()
        print(token.content, end="", flush=True)
    print()