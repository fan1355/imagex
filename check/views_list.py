
import os
import json
from django.http import HttpResponse

from check import util_file
import datetime

def checkList(request):
    resp = {"data":[]}
    result_dict = util_file.load_result()
    print(result_dict)
    for root,dirs,files in os.walk("check-img/"):
        for file in files:
            #获取文件所属目录
            print(root)
            #获取文件路径
            print(os.path.join(root,file))
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

