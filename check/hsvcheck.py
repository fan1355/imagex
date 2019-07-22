from cv2 import cv2
import numpy as np
import logging

from . import util as show
from . import colors

logger = logging.getLogger('cmd')

#轮廓面积计算函数
def areaCal(contour):

    area = 0
    for i in range(len(contour)):
        area += cv2.contourArea(contour[i])

    return area

def find_area(img, range_list):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = []
    for hsv_range in range_list:
        if len(mask) > 0:
            mask += cv2.inRange(hsv, hsv_range[0], hsv_range[1])
        else:
            mask = cv2.inRange(hsv, hsv_range[0], hsv_range[1])

    mask = cv2.medianBlur(mask,3)
    _, binary = cv2.threshold(mask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #在binary中发现轮廓，轮廓按照面积从小到大排列
    contours, _ = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    # print(len(contours))
    cv2.drawContours(img,contours,-1,(0,0,255),3)
    area_measure = areaCal(contours)
    return mask, area_measure

def docheck(img_path, color, std_area_measure):
    """
    返回值：1-通过；0-不通过；-1 图像不够清晰
    """
    color_range = colors.get_color_list(color)
    img = cv2.imread(img_path)
    _, area_measure = find_area(img, color_range)
    
    logger.info("%s color:[%s] real:[%s] std:[%s]" % (img_path, color, area_measure, std_area_measure))

    confidence = area_measure / std_area_measure
    if confidence > 0.5:
        return 1
    elif confidence > 0.2:
        return -1
    else:
        return 0


if __name__ == "__main__":
    # 绿色的范围
    # hsv_range_list = [(np.array([47, 65, 18]), np.array([96, 255, 153]))]
    # 红色范围
    # hsv_range_list = [(np.array([0, 170, 170]), np.array([7, 255, 255])), \
    #         (np.array([137, 170, 170]), np.array([180, 255, 255]))]
    # 蓝色范围
    # hsv_range_list = [(np.array([95, 130, 70]), np.array([166, 255, 255]))]
    # size = 3
    # std_area_measure = 41383.0
    

    # for i in range(size):
    #     file_path = 'img/cir/%s.jpeg' % (i+1)
    #     img = cv2.imread(file_path)
    #     show.set_plt(img, size, 3, (i*3+1), file_path)
        
    #     mask, area_measure = find_area(img, hsv_range_list)
    #     confidence = area_measure / std_area_measure
    #     # print((std_area_measure, area_measure, confidence))

    #     if confidence > 0.5:
    #         print("%s: 检测通过 (%s)" % (file_path, (std_area_measure, area_measure, confidence)))
    #     elif confidence > 0:
    #         print("%s: 请摆正后重试 (%s)" % (file_path, (std_area_measure, area_measure, confidence)))
    #     else:
    #         print("%s: 发现缺陷 (%s)" % (file_path, (std_area_measure, area_measure, confidence)))


    #     show.set_plt(mask, size, 3, (i*3+2), "mask")
    #     show.set_plt(img, size, 3, (i*3+3), "contours")
    
    # show.show_plt()
    pass





