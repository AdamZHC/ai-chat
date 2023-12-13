import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


os.environ["http_proxy"] = "http://127.0.0.1:33210"
os.environ["https_proxy"] = "http://127.0.0.1:33210"

API_KEY = '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'

from langchain.chat_models import ChatAnthropic



if __name__ == '__main__':
    # llm = OpenAI(max_tokens=1024, openai_api_key=API_KEY)
    # print(llm.predict("请你介绍“中文”"))
    # chat = ChatAnthropic()

    # steaming
    llm = ChatOpenAI(max_tokens=2048,
                     openai_api_key='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')

    # prompt = ChatPromptTemplate.from_messages(
    #     [("system", "你是一个专业的AI助手。"), ("human", "{query}")]
    # )

    # llm_chain = prompt | llm
    one_input_prompt = PromptTemplate(input_variables=["adjective"], template="Tell me a {adjective} joke.")
    prompt = one_input_prompt.format(adjective="funny")

    ret = llm.predict(prompt)
    print(ret)
    # for token in ret:
    #     print()
    #     print(token.content, end="", flush=True)
    # print()