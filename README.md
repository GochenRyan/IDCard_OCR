# IDCard_OCR
Intelligent identification and detection of ID card information

## 关键技术
1. Tesseract-OCR(识别字符)
2. 二值化算法池(二值化图像)
2. Flask(后端)
3. jQuery + Ajax(前端异步更新)

## 系统需求
1. windows或Linux
2. Python2.7
3. Tesseract-OCR
4. MySQL

## 安装
1. 从 https://github.com/GochenRyan/IDCard_OCR.git Clone项目
2. 部署环境 ```pip install -r requirements.txt```
3. 安装Tesseract-OCR
4. 根据安装地址更改 IDCard_OCR/include/functions.py 下ocr函数中TESSERACT_OCR变量
5. 安装MySQL
6. 根据数据库配置，更改 IDCard_OCR/dbOperate.py 中 connect_idcard_db函数
7. 创建local_config.py文件，配置数据库用户和密码