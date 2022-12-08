from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
from flask import Flask, Response, request, render_template
import os
import json
import time
from flask_cors import cross_origin


# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory


app = Flask(__name__)


@app.route('/')
def r():
    return render_template('ocr.html')


@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    img = request.files.get('photo') # 从post请求中获取图片数据
    suffix = '.' + img.filename.split('.')[-1] # 获取文件后缀名
    basedir = os.path.abspath(os.path.dirname(__file__)) # 获取当前文件路径
    photo = '/test/' + str(int(time.time())) + suffix # 拼接相对路径
    img_path = basedir + photo # 拼接图片完整保存路径,时间戳命名文件防止重复
    img.save(img_path) # 保存图片
    
    
    result = ocr.ocr(img_path, cls=True)
    # 显示结果
    
    result = result[0]
    t = ''
    for i in result:
        t += i[1][0]
        t += '\n'
    return {'msg':t}


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
