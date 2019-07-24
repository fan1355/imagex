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

def get_info(request):
    """
    检测标准图的色块位置信息
    """
    if request.method=='POST':
        param = request.POST
    elif request.method=='GET':
        param = request.GET
    else:
        param = {}

    color_dict = json.loads(param.get('colors',r"{}"))
    logger.info("%s" % (color_dict))
    # 处理图片
    file_source = request.FILES.get("picture")
    file_source.name = util_file.get_file_name(file_source.name)
    file_path = "check-img/"+file_source.name
    img_file = open(file_path, 'wb+')
    for chunk in file_source.chunks():  
        img_file.write(chunk)  
    img_file.close()
    # 分析图片信息
    list_size = len(color_dict.keys())
    if file_path and list_size > 0:
        info = movecheck.get_info(file_path, color_dict)
        return HttpResponse(json.dumps(info),content_type="application/json")
    else:
        return HttpResponse("ERR.")

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
    color_dict = json.loads(param.get('colors',r"{}"))
    # color_list = param.get('colors','').split(",")
    # scale_str = param.get('scale_str','[]')
    # std_rect_str = param.get('std_rect_str','[]')
    logger.info("colors: %s" % (color_dict))
    # 处理图片
    file_source = request.FILES.get("picture")
    file_source.name, file_type = util_file.get_file_name(file_source.name)
    file_path = "check-img/"+file_source.name
    img_file = open(file_path, 'wb+')
    for chunk in file_source.chunks():  
        img_file.write(chunk)  
    img_file.close()  

    list_size = len(color_dict.keys())
    if file_path and list_size > 0:
        # 根据检测结果，将图像合并
        rslt, _ = movecheck.docheck(file_path, color_dict)
        # return HttpResponse("%s" % rslt)
        with open(file_path, 'rb') as f:
            image_str = "data:image/%s;base64,%s" % (file_type, str(base64.b64encode(f.read()))[2:-1] )
        # logger.info("%s - %s ...... %s" % (type(image_str), image_str[:20], image_str[-20:]))
        resp = dict()
        resp["info"] = rslt
        resp["img"] = image_str
        return HttpResponse(json.dumps(resp),content_type="application/json")
                
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