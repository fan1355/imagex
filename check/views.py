from django.shortcuts import render
from django.http import HttpResponse
import  numpy as np
import logging
import json
import base64

from check import movecheck
from check import hsvcheck
from check import util_file
from check import multihsvcheck

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
    # 保存图片
    file_path, _, file_type = util_file.save_file_from_source(request.FILES.get("picture"))
    # 分析图片信息，生成返回图像
    list_size = len(color_dict.keys())
    if file_path and list_size > 0:
        info, _ = movecheck.get_info(file_path, color_dict)
        with open(file_path, 'rb') as f:
            image_str = "data:image/%s;base64,%s" % (file_type, str(base64.b64encode(f.read()))[2:-1] )
        resp = dict()
        resp["info"] = info
        resp["img"] = image_str

        logger.info("get info: %s, file: %s" % (info, file_path))
        return HttpResponse(json.dumps(resp),content_type="application/json")
    else:
        logger.info("get info error")
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
    std_size = json.loads(param.get('size',r"{}"))
    logger.info("colors: %s" % (color_dict))
    # 保存图片
    file_path, _, file_type = util_file.save_file_from_source(request.FILES.get("picture"))
    # 生成返回图像
    list_size = len(color_dict.keys())
    if file_path and list_size > 0:
        # 根据检测结果，将图像合并
        rslt, _ = movecheck.docheck(file_path, std_size, color_dict)
        # return HttpResponse("%s" % rslt)
        with open(file_path, 'rb') as f:
            image_str = "data:image/%s;base64,%s" % (file_type, str(base64.b64encode(f.read()))[2:-1] )
        # logger.info("%s - %s ...... %s" % (type(image_str), image_str[:20], image_str[-20:]))
        resp = dict()
        resp["info"] = rslt
        resp["img"] = image_str

        logger.info("position check result: %s, file: %s" % (resp["info"], file_path))
        return HttpResponse(json.dumps(resp),content_type="application/json")
    
    else:
        logger.info("position check error")
        return HttpResponse("ERR.")

def multi_hsv_check(request):
    """
    多个色块检测（颜色外部传入）
    """
    if request.method=='POST':
        param = request.POST
    elif request.method=='GET':
        param = request.GET
    else:
        param = {}
    # print("%s -- %s -- %s" % (request.method, str(request.GET), param ) )
    base64_str = param.get('img','')
    if base64_str != '':
        file_path = util_file.save_pic(base64_str)
    else:
        file_path, _, _ = util_file.save_file_from_source(request.FILES.get("picture"))

    # color_dict = json.loads(param.get('colors',''))
    # 读取标准文件
    color_dict = util_file.load_json("check-std/colors.json")
    if not len(color_dict.keys()) > 0:
        return HttpResponse("{'code': 'err','msg':'no std info'")
    print("%s -- %s -- %s" % (request.method, base64_str[0:100], color_dict))
    # print("%s -- %s -- %s" % (request.method, str(request.GET), color_dict ) )
    logger.info(color_dict)
    
    check_result = multihsvcheck.docheck(file_path, color_dict)

    logger.info("hsv check result: %s" % json.dumps(check_result))
    return HttpResponse("{'code': 'ok', 'file_path':'%s', 'result':'%s'}" % (file_path, check_result))


def hsv_check(request):
    """
    只检测色块是否存在（颜色已预置）
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
        
        logger.info("hsv check result: %s" % json.dumps(rslt))
        return HttpResponse("%s" % rslt)

    else:
        logger.info("hsv check error")
        return HttpResponse("ERR.")

def show_pic(request):
    """
    展示输入图片用
    """
    if request.method=='POST':
        param = request.POST
    elif request.method=='GET':
        param = request.GET
    else:
        param = {}
    
    file_name = param.get('name','not found')
    logger.info("show picture: %s" % (file_name))
    try:
        imagepath = "check-img/{}".format(file_name)  # 图片路径
        with open(imagepath, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/jpeg")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))



