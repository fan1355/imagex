# from django.test import TestCase

# Create your tests here.
from cv2 import cv2

from check import movecheck
from check import util as show

if __name__ == "__main__":
    rows = 2
    col_from = 11
    col_to = 13
    cols = col_to - col_from + 1

    # 标准距离
    # std_rect = (170, 464, 210, 214)  # x, y, w, h
    std_rect = (546, 383, 229, 231)
    # 比较精度
    x_scale = 0.1
    y_scale = 0.1

    # i = 0
    for i in range(cols):
        file_path = 'check-img/cir/%s.jpeg' % (i+col_from)
        color_list = ["green","orange"]
        std_rect_list = [
            {'x': 546, 'y': 383, 'w': 229, 'h': 231},    # green 4
            {'x': 93, 'y': 110, 'w': 228, 'h': 234},    # orange 4 (93, 110, 228, 234)
            
            # {'x': 172, 'y': 467, 'w': 209, 'h': 212},    # green 1 
            # {'x': 356, 'y': 671, 'w': 209, 'h': 211},    # orange 1
        ]
        scale_list = [{'x':0.1, 'y': 0.1}, {'x':0.1, 'y': 0.1}]
        rslt, draw_img = movecheck.docheck(file_path, color_list, std_rect_list, scale_list)

        show.set_plt(cv2.imread('check-img/cir/4.jpeg'), rows, cols, (i+1), "Correct example")
        # show.set_plt(mask, rows, cols, (i*cols+2), "mask")
        # show.set_plt(closed, rows, cols, (i*cols+3), "closed")
        # show.set_plt(cut_img, rows, cols, (i*cols+4), "cut")
        title = "Correct" if rslt else "Wrong"
        show.set_plt(draw_img, rows, cols, (i+cols+1), title)
        print(rslt)
    
    show.show_plt()