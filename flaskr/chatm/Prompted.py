from abc import ABC, abstractmethod
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

class BasePrompted(ABC):
    @abstractmethod
    def message_from_prompt(self, template, input_variables, **kwargs):
        pass
class StaticPrompted(BasePrompted):
    def message_from_prompt(self, template, input_variables, **kwargs):
        return PromptTemplate(template=template, input_variables=input_variables).format(**kwargs)

class SingletonPrompted(BasePrompted):
    def __init__(self, template, input_variables):
        self.__template__ = PromptTemplate(template=template, input_variables=input_variables)

    def message_from_prompt(self, **kwargs):
        return self.__template__.format(**kwargs)