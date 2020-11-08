
from cv2 import cv2
from check import preprocessing
import numpy as np
import logging
from check import util
from check import processor

logger = logging.getLogger('cmd')

def get_color(img, area_measure):
    """
    获取指定范围内的颜色信息

    """
    

def get_info(img_path, color_dict):
    """
    收集图片色块位置信息
    @return {"color":{x:1, y:1, w:10, h:10}}
    """
    rslt = dict()
    frame = cv2.imread(img_path)
    x, y, w, h = preprocessing.cut_background(frame.copy()) 
    rslt["size"] = {"w": w, "h": h}

    frame = frame[y:y+h, x:x+w]
    draw_img = frame.copy()
    info = dict()
    for color,range_list in color_dict.items():
        color_range = [(np.array(range[0]), np.array(range[1])) for range in range_list]
        logger.info("%s: %s" % (color, color_range))
        # 轮廓识别
        contours = processor.get_contours(frame, color_range)
        # 判断目标色块是否存在
        if len(contours) < 1:
            info[color] = None
        else:
            # 取最大色块轮廓，一般应该只有一个轮廓
            max_countor = sorted(contours, key=cv2.contourArea, reverse=True)[0]
            x, y, w, h = cv2.boundingRect(max_countor)
            info[color] = {"x": x, "y": y, "w": w, "h": h}
            # 绘制色块位置
            draw_img = util.draw_std_rect(draw_img, (x, y, w, h))

    rslt["position"] = info
    logger.info("%s info: %s" % (img_path, rslt))
    # 覆盖原始图像，保存识别后的图像
    # 通用方法，不修改原图 cv2.imwrite(img_path, draw_img)

    return rslt, draw_img