from django.shortcuts import render
from django.http import HttpResponse
import  numpy as np
import logging
import json
import base64

from check import movecheck
from check import hsvcheck
from check import util_file

logger = logging.getLogger('cmd') # 这里用__name__通用,自动检测.

def position_check(request):
    """
    同时检测 颜色和位置，只有都符合才通过
    """
    if request.method=='POST':
        param = request.POST
    elif request.method=='GET':
        param = request.GET
    else:
        param = {}
    # logger.info("%s -- %s -- %s" % (request.method, str(request.GET), param ) )
    color_list = param.get('colors','').split(",")
    scale_str = param.get('scale_str','[]')
    std_rect_str = param.get('std_rect_str','[]')
    logger.info("%s -- %s -- %s" % (color_list, scale_str, std_rect_str))
    # 处理图片
    file_source = request.FILES.get("picture")
    file_source.name = util_file.get_file_name(file_source.name)
    file_path = "check-img/"+file_source.name
    img_file = open(file_path, 'wb+')
    for chunk in file_source.chunks():  
        img_file.write(chunk)  
    img_file.close()  

    list_size = len(color_list)
    scale_list = json.loads(scale_str)
    std_rect_list = json.loads(std_rect_str)
    if file_path and list_size > 0 and len(scale_list) == list_size:
        # 根据检测结果，将图像合并
        rslt, _ = movecheck.docheck(file_path, color_list, std_rect_list, scale_list)
        # return HttpResponse("%s" % rslt)
        with open(file_path, 'rb') as f:
            image_str = str(base64.b64encode(f.read()))
        resp = dict()
        resp["info"] = rslt
        resp["img"] = image_str
        return HttpResponse(json.dumps(resp,ensure_ascii=False),content_type="application/json,charset=utf-8")
                
    return HttpResponse("ERR.")


def hsv_check(request):
    """
    只检测色块是否存在
    """
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

    file_path = util_file.save_pic(base64_str)
    list_size = len(color_list)
    if file_path and list_size > 0 and len(measure_list) == list_size:
        rslt = dict()
        for i in range(list_size):
            color = color_list[i]
            measure = int(measure_list[i])
            cf = hsvcheck.docheck(file_path, color, measure)
            rslt[color] = cf
        
        return HttpResponse("%s" % rslt)
                
    return HttpResponse("ERR.")