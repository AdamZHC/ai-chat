from flask import (
    Blueprint, request, Response
)
import json
from werkzeug.utils import secure_filename

bp = Blueprint('analyse', __name__)
# 初始化

# 上传简历
@bp.route('/upload', methods = ['POST'])
def upload_file():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    return '文件上传成功'

# AI点评
@bp.route('/comment', methods = ['GET'])
def comment():
    return '测试数据'

# AI推荐
@bp.route('/recommend', methods = ['GET'])
def recommend():
    return '测试数据'

# Try Again
@bp.route('/again', methods = ['GET'])
def again():
    return '测试数据'


