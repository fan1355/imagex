from cv2 import cv2
from check import hsvcheck
from check import util
from check import util_file
from check import preprocessing
import numpy as np

def docheck(img_path, color_std_area_measure_dict):
    """
    dict: {
        "red":{
                "area":[309, 298, 307, 89],
                "range":[ [[100, 141,   0], [180, 255, 255]] ],
                "std_measure": 23635.5
            }
    }

    return: check_result: [{"color": 1 }] 1-通过；0-未通过
    """
    img = cv2.imread(img_path)
    img = preprocessing.resize(img.copy(), 100, 100)

    measures = []
    check_result = dict()
    result = 0
    for color, value in color_std_area_measure_dict.items():
        # 获取参数
        x, y, w, h = value["area"][0], value["area"][1], value["area"][2], value["area"][3]
        color_range = [(np.array(range[0]), np.array(range[1])) for range in value["range"]]
        std_measure = value["std_measure"]

        # logger.info((x, y, w, h))

        # img_cut = img[y:y+h, x:x+w]
        # logger.info(img_cut)
        _, area_measure, contours = find_area(img, color_range)
        measures.append(area_measure)
        if area_measure / std_measure > 0.75:
            check_result[color] = 1
        else:
            check_result[color] = 0
            result += 1
        #  = area_measure / std_measure
        max_countor = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        cv2.drawContours(img,[max_countor],-1,(0,0,255),3)
    # 覆盖原始图像，保存识别后的图像
    cv2.imwrite(img_path, img)
    util_file.save_result(img_path, result)
    return check_result    

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
    area_measure = util.areaCal(contours)
    return img, area_measure, contours

