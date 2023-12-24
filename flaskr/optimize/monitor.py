from flaskr.chatm.ChatModel import (
    ChatModel, FixedTemplateChainChatModel
)
from flaskr.chatm.memory import (
    MemoryUtil
)
from flaskr.chatm.mfactory import (
    InstanceUtil
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
    def __init__(self, template, input_variables, memorable, stream=True):
        self.__memorable_obj__ = memorable
        super().__init__(template, input_variables, stream)
    def _memory_(self):
        return self.__memorable_obj__
    def memorable(self):
        return self._memory_()



# 单agent封装
class MonitorDecorator:
    def __init__(self, template, input_variables, feedback_template, feedback_table: dict):
        self.__common_memory__ = ConversationBufferMemory(memory_key=MemoryUtil.MEMORY_KEY)
        self.__agent__ = MemoryModifiableChatModel(template, input_variables, self.__common_memory__, True)
        self.__feedback_callable__ = FixedTemplateChainChatModel(feedback_template, list(["context", "ret"]), False)
        self.__feedback_table__ = feedback_table
    def predict(self, **kwargs):
        ret = InstanceUtil.get_chain(self.__agent__).predict(**kwargs)
        context = self.__common_memory__
        # 对应的回答key
        key = self.__feedback_callable__.predict(context=context, ret=ret)
        table = self.__feedback_table__
        if key in table.keys():
            table[key](self)
        else:
            table['default'](self)

class FeedbackAutoMachine:
    def __init__(self, template_dict, input_variables_dict, feedback_template, feedback_table: dict):
        self.__common_memory__ = ConversationBufferMemory(memory_key=MemoryUtil.MEMORY_KEY)
        self.__agent_dict__ = dict()
        for key in template_dict.keys():
            self.__agent_dict__[key] = FixedTemplateChainChatModel(template_dict[key], input_variables_dict[key])
        self.__feedback_callable__ = FixedTemplateChainChatModel(feedback_template, list(["context", "ret"]), False)
        self.__feedback_table__ = feedback_table
        # self.__common_memory__ = self.__agent__,
    def predict(self, **kwargs):
        # 聊天策略
        agent, mark = self.pop_policy()
        if mark:
            return agent.predict(**kwargs)
        else:
            ret = InstanceUtil.get_chain(agent).predict(**kwargs)
            context = self.__common_memory__
            # 对应的回答key
            key = self.__feedback_callable__.predict(context=context, ret=ret)
            table = self.__feedback_table__
            if key in table.keys():
                return table[key](self)
            else:
                return table['default'](self)

    def pop_policy(self):
        return self.__agent_dict__['default'], False





if __name__ == '__main__':
    print("Hello World")
