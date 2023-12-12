import os
from langchain.chat_models import ChatOpenAI
from chatm import Prompted
from config import ConfigRead


class BaseChatModel(ConfigRead.ConfigReader):
    # 初始化
    def __init__(self, stream=True):
        super().__init__()
        self.__API_KEY__ = self.property("api_key")
        self.__DEFAULT_TOKEN__ = self.property("token")
        os.environ["http_proxy"] = "http://127.0.0.1:{}".format(self.property("proxy_port"))
        os.environ["https_proxy"] = "http://127.0.0.1:{}".format(self.property("proxy_port"))
        self.__init_model__(stream)
    def __init_model__(self, stream=True):
        self.__llm__ = ChatOpenAI(max_tokens=self.__DEFAULT_TOKEN__, openai_api_key=self.__API_KEY__, streaming=stream)
    def predict(self, text) -> str:
        return self.__llm__.predict(text)

    def stream_predict(self, text):
        return self.__llm__.stream(text)

class MultiTemplateChatModel(BaseChatModel, Prompted.StaticPrompted):
    def __init__(self, stream=True):
        super().__init__(stream)
    # 提示词构造 父类实现提示词构造
    def text(self, template, input_variables, **kwargs):
        return self.message_from_prompt(template, input_variables, **kwargs)
    def answer(self, template, input_variables, **kwargs) -> str:
        text = self.text(template, input_variables, **kwargs)
        return self.predict(text)
    def stream_answer(self, template, input_variables, **kwargs):
        text = self.text(template, input_variables, **kwargs)
        return self.stream_predict(text)

class FixedTemplateChatModel(BaseChatModel, Prompted.SingletonPrompted):
    def __init__(self, template, input_variables, stream=True):
        super(BaseChatModel).__init__(stream)
        super(Prompted.SingletonPrompted).__init__(template, input_variables)
    # 提示词构造 父类实现提示词构造
    def answer(self, **kwargs) -> str:
        text = self.__template__(**kwargs)
        return self.predict(text)
    def stream_answer(self, **kwargs):
        text = self.__template__(**kwargs)
        return self.stream_predict(text)


if __name__ == '__main__':
    chat = BaseChatModel()
    ret = chat.stream_predict("请介绍中文")
    for token in ret:
        print(token.content, end="", flush=True)

