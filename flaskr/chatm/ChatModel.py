import os
from abc import ABC, abstractmethod
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from flaskr.chatm import (
    prompted, memory, mfactory
)
import asyncio
from langchain.callbacks import AsyncIteratorCallbackHandler
from flaskr.config import ConfigRead


# 聊天模型接口
class ChatModel(ABC):
    # 获取可执行模型
    @abstractmethod
    def __callable__(self):
        pass

    @abstractmethod
    def _predict_(self, text):
        pass


# 抽取公共初始化方法
class InitializedChatModel(ChatModel, ConfigRead.ConfigReader):
    # 初始化
    def __init__(self, stream=True):
        ConfigRead.ConfigReader.__init__(self)
        self.__API_KEY__ = self.property("api_key")
        self.__DEFAULT_TOKEN__ = self.property("token")
        self.__STREAM_MARK__ = stream
        # 回调处理接口
        os.environ["http_proxy"] = "http://127.0.0.1:{}".format(self.property("proxy_port"))
        os.environ["https_proxy"] = "http://127.0.0.1:{}".format(self.property("proxy_port"))
        self.__callable_obj__ = None

    @abstractmethod
    def __callable__(self):
        pass

    def _predict_(self, text):
        pass


# 基本聊天模型
class BaseChatModel(InitializedChatModel):

    def __callable__(self):
        if not self.__callable_obj__:
            self.__callable_obj__ = mfactory.InstanceUtil.new_chat(
                max_tokens=self.__DEFAULT_TOKEN__,
                openai_api_key=self.__API_KEY__,
                streaming=self.__STREAM_MARK__)
        if self.__STREAM_MARK__:
            self.__call_back__ = AsyncIteratorCallbackHandler()
            self.__callable_obj__ = mfactory.InstanceUtil.copy_chat(
                src=self.__callable_obj__, callback=self.__call_back__
            )
        return self.__callable_obj__

    def _predict_(self, text):
        m = self.__callable__()
        if self.__STREAM_MARK__:
            coro = m.apredict(text)
            task = asyncio.create_task(coro)
            return task, self.__call_back__
        else:
            return m.predict(text)

    def predict_(self, text):
        return self._predict_(text)


class ChainChatModel(InitializedChatModel):
    def __callable__(self):
        if not self.__callable_obj__:
            self.__callable_obj__ = mfactory.InstanceUtil.new_chain(
                max_tokens=self.__DEFAULT_TOKEN__,
                openai_api_key=self.__API_KEY__,
                streaming=self.__STREAM_MARK__,
                prompt=self._template_()
            )
        if self.__STREAM_MARK__:
            self.__call_back__ = AsyncIteratorCallbackHandler()
            self.__callable_obj__ = mfactory.InstanceUtil.copy_chain(
                src=self.__callable_obj__,
                callback=self.__call_back__
            )
        return self.__callable_obj__

    @abstractmethod
    def _template_(self):
        pass


class MultiTemplateChainChatModel(BaseChatModel, prompted.StaticPrompted):
    def __callable__(self):
        if not self.__callable_obj__:
            self.__callable_obj__ = mfactory.InstanceUtil.new_common_chain(
                max_tokens=self.__DEFAULT_TOKEN__,
                openai_api_key=self.__API_KEY__,
                streaming=self.__STREAM_MARK__,
            )
        if self.__STREAM_MARK__:
            self.__call_back__ = AsyncIteratorCallbackHandler()
            self.__callable_obj__ = mfactory.InstanceUtil.copy_common_chain(
                src=self.__callable_obj__,
                callback=self.__call_back__
            )
        return self.__callable_obj__

    # 提示词构造 父类实现提示词构造
    def predict(self, template, input_variables, **kwargs):
        text = self.message_from_prompt(template, input_variables, **kwargs)
        return self._predict_(text)


class FixedTemplateChainChatModel(ChainChatModel, prompted.SingletonPrompted):

    def __init__(self, template, input_variables, stream=True):
        ChainChatModel.__init__(self, stream)
        prompted.SingletonPrompted.__init__(self,
                                            memory.MemoryUtil.add_prefix_template(template),
                                            memory.MemoryUtil.add_prefix_input_variables(input_variables))

    def _template_(self):
        return self.__template__

    # 提示词构造 父类实现提示词构造
    def predict(self, **kwargs):
        m = self.__callable__()
        if self.__STREAM_MARK__:
            coro = m.apredict(**kwargs)
            task = asyncio.create_task(coro)
            return task, self.__call_back__
        else:
            return m.predict(**kwargs)


async def f():
    # chat = FixedTemplateChainChatModel("{text}", ['text'])
    chat = BaseChatModel()
    task, callback = chat.predict_(text='请写一首五言藏头诗')
    async for token in callback.aiter():
        print(token, end="")
    await task

    task, callback = chat.predict_(text='请分析该诗的特点')
    async for token in callback.aiter():
        print(token, end="")
    await task
    # print(text); text = ""
    # task, callback = chat.predict(text='请分析该诗的特点')
    # # print(ret)
    # async for token in callback.aiter():
    #     text += token
    # await task
    # print(text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(f())
    # LLMChain()
