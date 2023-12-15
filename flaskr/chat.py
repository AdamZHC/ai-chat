from flask import (
    Blueprint, request, Response
)
import queue
import asyncio
import json
import threading
from chatm import ChatModel

bp = Blueprint('chat', __name__)
local = threading.local()
local.q = queue.Queue()
# q = queue.Queue

@bp.route('/oneshot', methods=['GET', 'POST'])
def chat():
    chat_model = ChatModel.BaseChatModel()
    content = json.loads(request.get_data())['content'] if request.method == 'POST' else '请讲一个笑话'
    return chat_model.predict(content)

@bp.route('/stream', methods=['GET', 'POST'])
def chat_stream():
    content = json.loads(request.get_data())['content'] if request.method == 'POST' else '请讲一个笑话'
    asyncio.run(f(content))
    def generate():
        q = local.q
        while not q.empty:
            yield q.get(block = True, timeout = 5)
    return Response(generate())

async def f(content):
    chat_model = ChatModel.BaseChatModel()
    task, callback = chat_model.predict_(content)
    # chat = FixedTemplateChainChatModel("{text}", ['text'])
    q = local.q
    async for token in callback.aiter():
        q.put(token)
    await task