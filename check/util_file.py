import base64
import time

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
        return date_str, "jpeg"


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