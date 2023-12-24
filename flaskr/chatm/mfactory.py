from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from flaskr.chatm import (
    memory
)


class InstanceUtil:
    @staticmethod
    def new_chat(max_tokens, openai_api_key, streaming):
        return ChatOpenAI(max_tokens=max_tokens,
                          openai_api_key=openai_api_key,
                          streaming=streaming)

    @staticmethod
    def copy_chat(src, callback):
        return ChatOpenAI(max_tokens=src.max_tokens,
                          openai_api_key=src.openai_api_key,
                          streaming=src.streaming,
                          callbacks=[callback])

    @staticmethod
    def new_chain(max_tokens, openai_api_key, streaming, prompt, memory_):
        return LLMChain(
            llm=ChatOpenAI(max_tokens=max_tokens,
                           openai_api_key=openai_api_key,
                           streaming=streaming),
            prompt=prompt,
            verbose=True,
            memory=memory_,
        )

    @staticmethod
    def copy_chain(src, callback):
        return LLMChain(
            llm=ChatOpenAI(max_tokens=src.llm.max_tokens,
                           openai_api_key=src.llm.openai_api_key,
                           streaming=src.llm.streaming,
                           callbacks=[callback]),
            prompt=src.prompt,
            verbose=True,
            memory=src.memory,
        )

    @staticmethod
    def new_common_chain(max_tokens, openai_api_key, streaming, memory_):
        return LLMChain(
            llm=ChatOpenAI(max_tokens=max_tokens,
                           openai_api_key=openai_api_key,
                           streaming=streaming),
            verbose=True,
            memory=memory_,
        )

    @staticmethod
    def copy_common_chain(src, callback):
        return LLMChain(
            llm=ChatOpenAI(max_tokens=src.llm.max_tokens,
                           openai_api_key=src.llm.openai_api_key,
                           streaming=src.llm.streaming,
                           callbacks=[callback]),
            verbose=True,
            memory=src.memory,
        )

    @staticmethod
    def get_chain(src):
        return LLMChain(
            llm=ChatOpenAI(max_tokens=src.llm.max_tokens,
                           openai_api_key=src.llm.openai_api_key,
                           streaming=False),
            verbose=True,
            prompt=src.prompt,
            memory=src.memory,
        )

