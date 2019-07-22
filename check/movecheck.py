from cv2 import cv2
import math
import numpy as np
import logging

from check import colors

logger = logging.getLogger('cmd')

def get_contours(img, range_list):
    """
    根据颜色提取图像
    """
    # 从BGR转换到HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = []
    for hsv_range in range_list:
        if len(mask) > 0:
            mask += cv2.inRange(hsv, hsv_range[0], hsv_range[1])
        else:
            mask = cv2.inRange(hsv, hsv_range[0], hsv_range[1])

    _, binary = cv2.threshold(mask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # 定义结构元素 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10, 10))
    # 开闭运算，先开运算去除背景噪声，再继续闭运算填充目标内的孔洞
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel) 
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel) 

    # 在binary中发现轮廓，轮廓按照面积从小到大排列
    contours, _ = cv2.findContours(closed ,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    return contours

def check_offset(std_rect, check_rect, x_scale, y_scale):
    """
    色块位置比对，根据传入精度，判断偏移是否符合要求
    """
    x, y, w, h = std_rect[0], std_rect[1], std_rect[2], std_rect[3]
    x1, y1, w1, h1 = check_rect[0], check_rect[1], check_rect[2], check_rect[3]
    # 各方向偏移小于偏差，且 长/宽变化小于偏差
    if abs(x-x1)/w < x_scale and abs(y-y1)/h < y_scale and abs(w-w1)/w < x_scale and abs(h-h1)/h < y_scale:
        return True
    else:
        return False

def draw_std_rect(img, std_rect):
    """
    在标准位置处绘制矩形
    """
    x, y, w, h = std_rect[0], std_rect[1], std_rect[2], std_rect[3]
    return cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 5)

def docheck(img_path, color, x_scale, y_scale, std_rect):
    """
    同时检测 颜色和位置 是否正确
    x_scale, y_scale 横向精度/纵向精度
    std_rect = [x, y, w, h] 色块标准位置，左上顶点坐标及矩形长/宽
    """
    color_range = colors.get_color_list(color)
    frame = cv2.imread(img_path)

    contours = get_contours(frame, color_range)
    # 判断目标色块是否存在
    if len(contours) < 1:
        draw_img = draw_std_rect(frame.copy(), std_rect)
        font = cv2.FONT_HERSHEY_SIMPLEX
        draw_img = cv2.putText(draw_img, 'X', (std_rect[0], std_rect[1]+std_rect[3]), font, 8, (0, 0, 255), 15)
        return False, draw_img

    # 取最大色块轮廓，一般应该只有一个轮廓
    max_countor = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    x, y, w, h = cv2.boundingRect(max_countor)
    if check_offset(std_rect, (x, y, w, h), x_scale, y_scale):
        # 测试通过
        draw_img = draw_std_rect(frame.copy(), std_rect)
        return True, draw_img
    else:
        draw_img = draw_std_rect(frame.copy(), std_rect)
        font = cv2.FONT_HERSHEY_SIMPLEX
        draw_img = cv2.putText(draw_img, 'X', (x, y+h), font, 8, (0, 0, 255), 15)
        return False, draw_img
