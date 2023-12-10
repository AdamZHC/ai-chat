import os
from langchain.chat_models import ChatOpenAI

class ChatModel:
    def __init__(self, stream=True):
        self.__API_KEY__ = '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'
        self.__DEFAULT_TOKEN__ = 1 << 10
        os.environ["http_proxy"] = "http://127.0.0.1:33210"
        os.environ["https_proxy"] = "http://127.0.0.1:33210"
        self.__init_model__(stream)
    def __init_model__(self, stream=True):
        self.__llm__ = ChatOpenAI(max_tokens=self.__DEFAULT_TOKEN__, openai_api_key=self.__API_KEY__, streaming=stream)

    def answer(self, text):
        return self.__llm__.predict(text)

    def stream_answer(self, text):
        return self.__llm__.stream(text)

if __name__ == '__main__':
    chat = ChatModel()
    ret = chat.stream_answer("请介绍中文")
    for token in ret:
        print(token.content, end="", flush=True)
