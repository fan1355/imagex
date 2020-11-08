import matplotlib.pyplot as plt
from cv2 import cv2 

# 显示识别效果
def set_plt(img, rows=1, cols=1, index=1, title="img"):
    img_show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.subplot(rows, cols, index)
    plt.imshow(img_show)
    plt.title(title)
    
def show_plt():
    plt.show()

def show(img):
    img_show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_show)
    plt.show()

#轮廓面积计算函数
def areaCal(contour):

    area = 0
    for i in range(len(contour)):
        area += cv2.contourArea(contour[i])

    return area

def draw_std_rect(img, std_rect):
    """
    在标准位置处绘制矩形
    """
    x, y, w, h = std_rect[0], std_rect[1], std_rect[2], std_rect[3]
    return cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 5)



