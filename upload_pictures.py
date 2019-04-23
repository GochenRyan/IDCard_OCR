# coding:utf-8
import copy
import random
import uuid

import demjson as demjson
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import json
import ocr
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from datetime import timedelta
import dbOperate as dbo

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
global upload_path

@app.route('/', methods=['POST', 'GET'])  # 添加路由
def index():
    return render_template("index.html")

@app.route('/upload/', methods=['POST', 'GET'])  # 添加路由
def upload():
    # 存储身份证图片
    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return 'error_type'
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        global upload_path
        upload_path = os.path.join(basepath, 'static\images', str(uuid.uuid1()) + '.jpg')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
    return 'success_type'

@app.route('/analysis/',methods=['POST'])
def analysis():
    # 返回解析数据：1. 解析过程 2. 证件信息 3. 提示信息
    global upload_path
    cardInfo = ocr.idCardOCR(upload_path)
    # 存入数据库的图片路径进行转义
    cardInfodb = copy.deepcopy(cardInfo)
    cardInfodb['face'] = cardInfodb['face'].replace('\\','\\\\')
    dbo.inset_cardinfo(cardInfodb)
    cardInfo = json.dumps(cardInfo, ensure_ascii=False)
    print cardInfo


    return cardInfo

@app.route('/modify/',methods=['POST', 'GET'])
def modify():
    # 验证修改的信息
    # 将可用数据存入数据库


    return ''

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')