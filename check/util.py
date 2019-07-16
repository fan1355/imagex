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