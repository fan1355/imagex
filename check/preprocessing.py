from cv2 import cv2
import numpy as np

def resize(img, w, h):
    """
    剪裁图像并重新调整大小
    """
    x, y, w, h = cut_background(img)
    img = img[y:y+h, x:x+w]
    return cv2.resize(img,(w,h),interpolation=cv2.INTER_CUBIC)

def cut_background(img):
    """
    @return x, y, w, h
    """
    h, w = img.shape[:2]
    mask=np.zeros((img.shape[:2]),np.uint8)
    bgdModel=np.zeros((1,65),np.float64)
    fgdModel=np.zeros((1,65),np.float64)
    rect=(100,100,w,h)
    # 多次计算，保证计算准确度
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,3,cv2.GC_INIT_WITH_RECT)
    #关于where函数第一个参数是条件，满足条件的话赋值为0，否则是1。如果只有第一个参数的话返回满足条件元素的坐标。
    mask2=np.where((mask==2)|(mask==0),0,1).astype('uint8')

    # 绘制轮廓
    draw_img=img*mask2[:,:,np.newaxis]
    h, w = draw_img.shape[:2]
    draw_img = cv2.cvtColor(draw_img, cv2.COLOR_BGR2GRAY)  #得到灰度图
    _, binary = cv2.threshold(draw_img,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
    if len(contours) < 1:
        return img
    else:
        max_countor = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        return cv2.boundingRect(max_countor)
