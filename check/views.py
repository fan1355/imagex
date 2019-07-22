from django.shortcuts import render
from django.http import HttpResponse
import  numpy as np
import logging

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
    measure_list = param.get('measures','').split(",")
    base64_str = param.get('img','not found')
    logger.info("%s -- %s -- %s" % (color_list, measure_list, base64_str[0:20]))
    file_path = util_file.save_pic(base64_str)
    list_size = len(color_list)
    if file_path and list_size > 0 and len(measure_list) == list_size:
        rslt = dict()


        # TODO 根据检测结果，将图像合并


        for i in range(list_size):
            color = color_list[i]
            measure = int(measure_list[i])
            cf = hsvcheck.docheck(file_path, color, measure)
            rslt[color] = cf
        
        return HttpResponse("%s" % rslt)
                
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