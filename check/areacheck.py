from cv2 import cv2
import numpy as np
import logging

from . import util
from . import colors

logger = logging.getLogger('cmd')


def docheck(img_path, color, std_area_measure):
    """
    返回值：1-通过；0-不通过；-1 图像不够清晰
    """
    color_range = colors.get_color_list(color)
    img = cv2.imread(img_path)
    _, area_measure = util.find_area(img, color_range)
    
    logger.info("%s color:[%s] real:[%s] std:[%s]" % (img_path, color, area_measure, std_area_measure))

    confidence = area_measure / std_area_measure
    if confidence > 0.5:
        return 1
    elif confidence > 0.2:
        return -1
    else:
        return 0
