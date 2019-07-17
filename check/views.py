from django.shortcuts import render
from django.http import HttpResponse
import base64
import time
import  numpy as np
import logging

from . import hsvcheck

logger = logging.getLogger('cmd') # 这里用__name__通用,自动检测.

def check(request):
    img_dir = "check-img/"
    # logger.info("%s -- %s -- %s" % (request.method, str(request.GET), str(request.POST) ) )
    if request.method=='POST':
        param = request.POST
    elif request.method=='GET':
        param = request.GET
    else:
        param = {}
    # logger.info("%s -- %s -- %s" % (request.method, str(request.GET), param ) )
    color_list = param.get('colors','').split(",")
    measure_list = param.get('measures','').split(",")
    base64_str = param.get('img','not found')
    logger.info("%s -- %s -- %s" % (color_list, measure_list, base64_str[0:20]))

    if base64_str != 'not found':
        # 去掉字符串开头的 data:image/png;base64,iVBO…… 这些信息
        base64_image = base64_str[base64_str.find(',')+1:]
        img_type = base64_str[base64_str.find('/')+1:base64_str.find(';')]
        # print(img_type)
        # 解码图片并保存
        decode_base64 = base64.b64decode(base64_image)
        # print(decode_base64)
        fmt='check-%Y%m%d-%H%M%S'      #定义时间显示格式
        date_str=time.strftime(fmt,time.localtime())     #把传入的元组按照格式，输出字符串
        file_path = img_dir+date_str+'.'+img_type
        file=open(file_path,'wb')  
        file.write(decode_base64)  
        file.close()

        list_size = len(color_list)
        if list_size > 0 and len(measure_list) == list_size:
            rslt = dict()
            for i in range(list_size):
                color = color_list[i]
                measure = int(measure_list[i])
                cf = hsvcheck.docheck(file_path, color, measure)
                rslt[color] = cf
            
            return HttpResponse("%s" % rslt)
                
    return HttpResponse("ERR.")