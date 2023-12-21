from flaskr.chatm.ChatModel import (
    ChatModel, FixedTemplateChainChatModel
)
from flaskr.chatm.memory import (
    MemoryUtil
)
from abc import (
    ABC, abstractmethod
)
from langchain.memory import ConversationBufferMemory
# 空接口
class MemoryModifiable(ABC):
    @abstractmethod
    def memorable(self):
        pass

class MemoryModifiableChatModel(FixedTemplateChainChatModel, MemoryModifiable):
    def __init__(self, template, input_variables, stream=True):
        self.__memorable_obj__ = ConversationBufferMemory(memory_key=MemoryUtil.MEMORY_KEY)
        super().__init__(template, input_variables, stream)
    def _memory_(self):
        return self.__memorable_obj__
    def memorable(self):
        return self._memory_()



# 单agent封装
class MonitorDecorator:
    def __init__(self, template, input_variables, feedback_template, feedback_input_variables):
        self.__agent__ = MemoryModifiableChatModel(template, input_variables, False)
        self.__feedback__ = FixedTemplateChainChatModel(feedback_template, feedback_input_variables, False)
        self.__common_memory__ = self.__agent__,
    def predict(self, **kwargs):
        ret = self.__agent__.predict(**kwargs)
        history = self.__common_memory__
        mark = self.__feedback__.predict(context = history, text=ret)
        if self.check_mark(mark):
            pass
        else:
            pass
    def check_mark(self, mark):
        pass

class FeedbackAutoMachine:
    def __init__(self, templates, input_variables_list, feedback_template, feedback_input_variables):
        # self.__agent__ = MemoryModifiableChatModel(template, input_variables, False)
        self.__feedback__ = FixedTemplateChainChatModel(feedback_template, feedback_input_variables, False)
        # self.__common_memory__ = self.__agent__,





if __name__ == '__main__':
    print("Hello World")
