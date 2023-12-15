import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler, AsyncIteratorCallbackHandler
from langchain.chains import LLMChain
import os
from abc import ABC, abstractmethod
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from flaskr.chatm import (
    prompted, memory
)
import asyncio
from langchain.callbacks import AsyncIteratorCallbackHandler
from flaskr.config import ConfigRead


API_KEY = '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'

from langchain.chat_models import ChatAnthropic

os.environ["http_proxy"] = "http://127.0.0.1:33210"
os.environ["https_proxy"] = "http://127.0.0.1:33210"

if __name__ == '__main__':
    # llm = OpenAI(max_tokens=1024, openai_api_key=API_KEY)
    # print(llm.predict("请你介绍“中文”"))
    # chat = ChatAnthropic()

    # steaming
    llm = OpenAI(max_tokens=2048,
                     openai_api_key='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',
                 streaming=True)

    # prompt = ChatPromptTemplate.from_messages(
    #     [("system", "你是一个专业的AI助手。"), ("human", "{query}")]
    # )

    # llm_chain = prompt | llm
    # one_input_prompt = PromptTemplate(input_variables=["adjective"], template="Tell me a {adjective} joke.")
    # prompt = one_input_prompt.format(adjective="funny")
    # for token in ret:
    #     print(token.content, end="", flush=True)
    m = LLMChain(llm=llm, callbacks=[StreamingStdOutCallbackHandler()], prompt=PromptTemplate(template="{text}", input_variables=['text']))
    print(m)
    m.callbacks = [AsyncIteratorCallbackHandler()]
    print(m)


