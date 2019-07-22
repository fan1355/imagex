import base64
import time

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