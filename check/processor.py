
from cv2 import cv2

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
