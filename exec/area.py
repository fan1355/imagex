# import sys
# sys.path.append("../check/")

from check import hsvcheck
from check import movecheck
from check import util
from check import extractcolor
from check.util_show import PicWin
from check import multihsvcheck, preprocessing

import numpy as np
import logging
from cv2 import cv2

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s')

logger = logging.getLogger('cmd')

color_dict = {
        # 绿色的范围
        "green": [(np.array([47, 65, 18]), np.array([96, 255, 153]))],
        # 红色范围
        "red": [
                (np.array([0, 43, 46]), np.array([10, 255, 255])),
                (np.array([156, 43, 46]), np.array([180, 255, 255]))
            ],
        # 蓝色范围
        "blue": [(np.array([95, 130, 70]), np.array([166, 255, 255]))],
        # 白色
        "white": [(np.array([0, 0, 221]), np.array([180, 30, 255]))],
        # 橙色
        # "orange": [(np.array([11, 43, 46]), np.array([25, 255, 255]))],
        "orange": [
            (np.array([6, 123, 110]), np.array([43, 255, 170])),
            (np.array([9, 111, 193]), np.array([180, 255, 255])),
        ], # test
        # 黄色
        "yellow": [(np.array([26, 43, 46]), np.array([34, 255, 255]))],
        # 紫色
        "purple": [(np.array([125, 43, 46]), np.array([155, 255, 255]))],

    }

def avg_color():
    img = cv2.imread("/Users/fan/python-workspace/imagex/check-img/check-20190724-151705.jpeg")
    x, y, w, h = 260, 1390, 600, 40
    img_cut = img[y:y+h, x:x+w]
    hsv = cv2.cvtColor(img_cut, cv2.COLOR_RGB2HSV)
    H, S, V = cv2.split(hsv)
    # 数值列表
    h = H.ravel()[np.flatnonzero(V)]
    h.sort()
    average_h  = sum(h)/len(h)
    logger.info("{}, size: {}".format(h, len(h)))
    logger.info(average_h)

    s = S.ravel()[np.flatnonzero(V)]
    s.sort()
    average_s  = sum(s)/len(s)
    logger.info("{}, size: {}".format(s, len(s)))
    logger.info(average_s)

    v = V.ravel()[np.flatnonzero(V)]
    v.sort()
    average_v  = sum(v)/len(v)
    logger.info("{}, size: {}".format(v, len(v)))
    logger.info(average_v)

    win = PicWin(1, 2)
    win.add(img, "img")
    win.add(img_cut, "cut")
    win.show()


if __name__ == "__main__":
    # "/Users/fan/python-workspace/imagex/check-img/check-20190724-151705.jpeg"
    # rslt, img_frame = extractcolor.get_info("/Users/fan/python-workspace/imagex/check-img/check-20190724-151705.jpeg", color_dict)
    # win = PicWin(1, 2)
    # win.add(img_frame, "get_info")
    # win.show()
    measure_dict = {
            "red":{
                "area":[309, 298, 307, 89],
                "range":[ [[100, 141,   0], [180, 255, 255]] ],
                "std_measure": 23635.5
            },
            "orange": {
                "area": [242, 687, 143, 463],
                "range": [[[0, 184, 0], [43, 255, 255]]],
                "std_measure": 60932.5,
            }
        }
    # multihsvcheck.docheck("/Users/fan/python-workspace/imagex/check-img/check-20190725-014637.jpeg", measure_dict)
    # img_path = "/Users/fan/python-workspace/imagex/check-img/check-20190724-151705.jpeg"
    win = PicWin(1, 2)

    img_path = "/Users/fan/python-workspace/imagex/check-img/WechatIMG503.jpeg"
    img = cv2.imread(img_path)
    img = preprocessing.resize(img.copy(), 100, 100)
    win.add(img, "background")

    img = cv2.imread(img_path)
    win.add(img, "orgin")
    measures = []
    check_result = dict()
    for color, value in measure_dict.items():
        # 获取参数
        x, y, w, h = value["area"][0], value["area"][1], value["area"][2], value["area"][3]
        color_range = [(np.array(range[0]), np.array(range[1])) for range in value["range"]]
        std_measure = value["std_measure"]

        # logger.info((x, y, w, h))

        # img_cut = img[y:y+h, x:x+w]
        # logger.info(img_cut)
        _, area_measure = hsvcheck.find_area(img, color_range)
        measures.append(area_measure)
        check_result[color] = area_measure / std_measure
    logger.info(measures)
    logger.info(check_result)

    win.show()

