# coding:utf-8
import copy

from flask import Flask, render_template, request
import os
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
upload_path = {}

@app.route('/', methods=['POST', 'GET'])  # 添加路由
def index():
    return render_template("index.html")

@app.route('/upload/', methods=['POST'])  # 添加路由
def upload():
    # 暂存身份证图片
    f = request.files['file']
    uuid = str(request.form.get('uuid'))
    if not (f and allowed_file(f.filename)):
        return 'error_type'
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    upload_path[uuid] = os.path.join(basepath, 'static\images', uuid + '.jpg')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path[uuid])
    return 'success_type'

@app.route('/analysis/',methods=['POST'])
def analysis():
    # 返回解析数据：1. 解析过程 2. 证件信息
    uuid = str(request.get_data())
    print upload_path[uuid]
    cardInfo = ocr.idCardOCR(uuid, upload_path[uuid])
    del upload_path[uuid]
    # 存入数据库的图片路径进行转义
    cardInfodb = copy.deepcopy(cardInfo)
    cardInfodb['face'] = cardInfodb['face'].replace('\\', '\\\\')
    dbo.inset_cardinfo(cardInfodb)
    cardInfo = json.dumps(cardInfo, ensure_ascii=False)
    print cardInfo


    return cardInfo

@app.route('/modify/',methods=['POST'])
def modify():
    # 验证修改的信息
    # 将可用数据存入数据库
    data = request.get_data()
    json_str = json.dumps(data)
    ojt = json.loads(json_str).encode('utf-8')
    info = json.loads(ojt)
    info['year'] = int(info['year'])
    info['month'] = int(info['month'])
    info['day'] = int(info['day'])
    print info
    dbo.update_cardinfo(info)
    return ''

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')