# -*- coding:utf-8 -*- 
#  @Time : 2018-01-09 11:59
#  @Author : Khazix
#  @File : ocr.py
#  @Description:
#            
#   --Input:
#   --Output:

from urllib import request
import base64
from PIL import Image
import json
import time
from threading import Thread


def get_ocr_result(imagebytes):
    # 压缩编码
    ls_f = base64.b64encode(imagebytes)
    s = bytes.decode(ls_f)

    host = 'http://tysbgpu.market.alicloudapi.com'
    path = '/api/predict/ocr_general'
    method = 'POST'
    appcode = 'fdb3ac38f5b647f7976b0c374349a02f'
    querys = 'code=74e51a88-41ec-413e-b162-bd031fe0407e'
    bodys = {}
    url = host + path + '?' + querys

    bodys[''] = "{\"uid\":\"118.12.0.12\",\"lang\":\"chns\",\"color\":\"color\",\"image\":\"" + s + "\"}"
    post_data = bodys['']
    req = request.Request(url, str.encode(post_data))
    req.add_header('Authorization', 'APPCODE ' + appcode)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    req.add_header('Content-Type', 'application/octet-stream')
    response = request.urlopen(req)
    # content = response.read()
    # if (content):
    #     content = str(content, 'utf-8')
    #     print(content)
    return response


def ocr_result(path):
    im = Image.open(path)
    im = im.convert('L')
    img_size = im.size
    w = im.size[0]
    h = im.size[1]
    # print("xx:{}".format(img_size))

    #冲顶大会
    # que_region = im.crop((50, 175, w - 50, 280))  # 裁剪的区域
    # ans_region = im.crop((50, 280, w - 50, 550))
    # # #百万英雄
    que_region = im.crop((50, 175, w - 50, 290))  # 裁剪的区域
    ans_region = im.crop((50, 290, w - 50, 620))
    #芝士超人
    # que_region = im.crop((50, 175, w - 50, 280))  # 裁剪的区域
    # ans_region = im.crop((50, 280, w - 50, 550))

    que_region.save("./que.png")
    ans_region.save("./ans.png")
    que_img = open('./que.png', 'rb')
    ans_img = open('./ans.png', 'rb')
    que_content = json.load(get_ocr_result(que_img.read()))
    ans_content = json.load(get_ocr_result(ans_img.read()))
    # print(que_content.keys())
    # print(que_content['ret'])

    question = ''
    for queblock in que_content['ret']:
        question += queblock['word']
    # print(question)

    answer = []
    for ansblock in ans_content['ret']:
        answer.append(ansblock['word'])
    # print(answer)
    return question, answer


if __name__ == '__main__':
    ocr_result(r"./timg.jpg")
