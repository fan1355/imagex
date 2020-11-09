import base64
import time
import json

def get_file_name(file_name):
    find_type = False
    fmt='check-%Y%m%d-%H%M%S'      #定义时间显示格式
    date_str=time.strftime(fmt,time.localtime())
    for c in file_name:
        if c == '.':
            find_type = True
    if find_type:
        file_type = file_name.split('.')[-1]
        return date_str + '.' + file_type, file_type
    else:
        return date_str + '.jpeg', "jpeg"

def save_file_from_source(file_source):
    """
    @return file_path, file_name, file_type
    """
    file_name, file_type = get_file_name(file_source.name)
    file_path = "check-img/"+file_name
    img_file = open(file_path, 'wb+')
    for chunk in file_source.chunks():  
        img_file.write(chunk)  
    img_file.close()

    return file_path, file_name, file_type

def save_result(imgPath, result):
    """
    """
    file_path = "check-img/result.dat"
    load_dict = load_result()
    key = imgPath[imgPath.index("/")+1:]
    load_dict[key] = result
    with open(file_path, "w") as dump_f:
        json.dump(load_dict,dump_f)

def load_result():
    file_path = "check-img/result.dat"
    try:
        with open(file_path, 'r') as load_f:
            load_dict = json.load(load_f)
    except IOError:
        load_dict = dict()
    return load_dict

def save_pic(base64_str):
    img_dir = "check-img/"

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

        return file_path
    else:
        return None