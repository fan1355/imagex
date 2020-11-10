
import os
import json
from django.http import HttpResponse

from check import util_file, multihsvcheck
import datetime
import base64
import logging

logger = logging.getLogger("cmd")

def checkList(request):
    resp = {"data":[]}
    result_dict = util_file.load_result()
    print(result_dict)
    for root, dirs, files in os.walk("check-img/"):
        for file in files:
            #获取文件所属目录
            print(root)
            #获取文件路径
            print(os.path.join(root, file))
            path = str(file)
            if not path.startswith("check"):
                continue
            rslt = -1
            if path in result_dict.keys():
                rslt = result_dict[path]
            
            rec = {
                "id": path,
                "std_id": "std_pic",
                "name": "工件",
                "time":path[path.index("-")+1 : path.index(".")],
                "woker": "001",
                "result":rslt
            }
            resp["data"].append(rec)
        break
    return HttpResponse(json.dumps(resp))


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
    base64_str = param.get('img','')
    if base64_str != '':
        file_path = util_file.save_pic(base64_str)
    else:
        file_path = util_file.save_std_file_from_source(request.FILES.get("picture"))
    # 分析图片信息，生成返回图像
    list_size = len(color_dict.keys())
    if file_path and list_size > 0:
        rslt, _ = multihsvcheck.get_info(file_path, color_dict)
        resp = dict()
        resp["info"] = rslt
        util_file.save_json("check-std/colors.json", rslt["position"])
        logger.info("get info: %s, file: %s" % (rslt, file_path))
        return HttpResponse(json.dumps(resp),content_type="application/json")
    else:
        logger.info("get info error")
        return HttpResponse("ERR.")

