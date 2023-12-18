import time

from flask import (
    Blueprint, request, Response
)
import queue
import asyncio
import json
import threading
from service.ChatService import ChatService

bp = Blueprint('chat', __name__)
# 初始化
service = ChatService()
service.init_single_session("{text}", ['text'])
service.init_serial_session("{text}", ['text'])

@bp.route('/single', methods=['GET', 'POST'])
def chat_single():
    content = json.loads(request.get_data())['content'] if request.method == 'POST' else '请讲一个笑话'
    return stream(0, content)

@bp.route('/serial', methods=['GET', 'POST'])
def chat_serial():
    content = json.loads(request.get_data())['content'] if request.method == 'POST' else '请讲一个笑话'
    return stream(1, content)

def stream(func_type, content):
    q = queue.Queue()
    threading.Thread(target=CoroutineTask, args=(func_type, content, q)).start()

    def generate():
        while True:
            try:
                token = q.get(block=True, timeout=3)
                yield token
            except queue.Empty:
                break

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(generate(), mimetype="text/event-stream", headers=headers)
def CoroutineTask(func_type, content, q):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(f(func_type, content, q))

async def f(func_type, content, q):
    if func_type == 0:
        task, callback = service.chat_single_session(text=content)
    else:
        task, callback = service.chat_serial_session(text=content)
    async for token in callback.aiter():
        # print(token, end="")
        q.put(token)
    await task