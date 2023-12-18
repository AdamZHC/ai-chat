from abc import ABC, abstractmethod
import json

from langchain.memory import ChatMessageHistory
from langchain.schema import messages_to_dict

class Serializable(ABC):
    def __load__(self):
        memory = self.__memorized__()
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for message in data:
                if message.type == "human":
                    memory.chat_memory.add_user_message(message.data.content)
                if message.type == "ai":
                    memory.chat_memory.add_ai_message(message.data.content)
    def __dump__(self):
        memory = self.__memorized__()
        dicts = messages_to_dict(memory.chat_memory.messages)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(dicts, f)
    @abstractmethod
    def __memorized__(self):
        pass


# 可持久化
# if __name__ == '__main__':
    # history.add_user_message("hi!")
    # history.add_ai_message("whats up?")
    # dicts = messages_to_dict(history.messages)
    # with open('data.json', 'w') as f:
    #     json.dump(dicts,f)

    # with open('data.json', 'r') as f:
    #     data = json.load(f)
    #     print(type(data))