from flask import (
    Blueprint, request, Response
)
import json
from chatm import ChatModel

bp = Blueprint('chat', __name__)

@bp.route('/oneshot', methods=['GET', 'POST'])
def chat():
    chat_model = ChatModel.BaseChatModel()
    content = json.loads(request.get_data())['content'] if request.method == 'POST' else '请讲一个笑话'
    return chat_model.predict(content)

@bp.route('/stream', methods=['GET', 'POST'])
def chat_stream():
    content = json.loads(request.get_data())['content'] if request.method == 'POST' else '请讲一个笑话'
    chat_model = ChatModel.BaseChatModel()
    res = chat_model.stream_predict(content)
    def generate():
        for trunk in res:
            yield trunk.content
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(generate(), mimetype="text/event-stream", headers=headers)

