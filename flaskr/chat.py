import time

from flask import (
    Blueprint, request, Response
)
import queue
import asyncio
import json
import threading
from chatm import ChatModel

bp = Blueprint('chat', __name__)
# q = queue.Queue

@bp.route('/oneshot', methods=['GET', 'POST'])
def chat():
    chat_model = ChatModel.BaseChatModel()
    content = json.loads(request.get_data())['content'] if request.method == 'POST' else '请讲一个笑话'
    return chat_model.predict(content)

@bp.route('/stream', methods=['GET', 'POST'])
def chat_stream():
    content = json.loads(request.get_data())['content'] if request.method == 'POST' else '请讲一个笑话'
    q = queue.Queue()
    threading.Thread(target=CoroutineTask,args=(content,q)).start()
    def generate():
        while True:
            token = q.get(block = True, timeout = 5)
            yield token

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(generate(), mimetype="text/event-stream", headers=headers)

def CoroutineTask(content, q):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(f(content, q))


async def f(content, q):
    chat_model = ChatModel.BaseChatModel()
    task, callback = chat_model.predict_(content)
    # chat = FixedTemplateChainChatModel("{text}", ['text']
    async for token in callback.aiter():
        print(token, end="")
        q.put(token)