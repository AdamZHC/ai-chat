from flaskr.chatm.ChatModel import (
    FixedTemplateChainChatModel, SerialChatModel
)

class ChatService:
    def __init__(self):
        # 单一对话
        self.single_session_mark = False
        self.single_session_model = None
        # 持久化
        self.serial_session_mark = False
        self.serial_session_model = None
    def init_single_session(self, template, input_variables):
        self.single_session_mark = True
        self.single_session_model = FixedTemplateChainChatModel(template, input_variables)
    def chat_single_session(self, **kwargs):
        return self.single_session_model.predict(**kwargs)

    def init_serial_session(self, template, input_variables):
        self.serial_session_mark = True
        self.serial_session_model = SerialChatModel(template, input_variables)

    def chat_serial_session(self, **kwargs):
        return self.serial_session_model.predict(**kwargs)


