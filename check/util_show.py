import matplotlib.pyplot as plt
from cv2 import cv2 

class PicWin():
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self._index = 1
    
    def add(self, img, title):
        plt.subplot(self.rows, self.cols, self._index)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(title)
        self._index += 1
    
    def show(self):
        plt.show()
