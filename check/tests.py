# from django.test import TestCase

# Create your tests here.
from cv2 import cv2

from check import movecheck
from check import util as show

if __name__ == "__main__":
    rows = 2
    cols = 7

    # 标准距离
    # std_rect = (170, 464, 210, 214)  # x, y, w, h
    std_rect = (546, 383, 229, 231)
    # 比较精度
    x_scale = 0.1
    y_scale = 0.1

    # i = 0
    for i in range(cols):
        file_path = 'check-img/cir/%s.jpeg' % (i+1)
        rslt, draw_img = movecheck.docheck(file_path, "green", x_scale, y_scale, std_rect)

        show.set_plt(cv2.imread('check-img/cir/1.jpeg'), rows, cols, (i+1), "Correct example")
        # show.set_plt(mask, rows, cols, (i*cols+2), "mask")
        # show.set_plt(closed, rows, cols, (i*cols+3), "closed")
        # show.set_plt(cut_img, rows, cols, (i*cols+4), "cut")
        title = "Correct" if rslt else "Wrong"
        show.set_plt(draw_img, rows, cols, (i+cols+1), title)
    
    show.show_plt()