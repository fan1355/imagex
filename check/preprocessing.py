from cv2 import cv2
import numpy as np

def resize(img, w, h):
    """
    剪裁图像并重新调整大小
    """
    x, y, w, h = cut_background(img)
    img = img[y:y+h, x:x+w]
    return cv2.resize(img,(w,h),interpolation=cv2.INTER_CUBIC)

def cut_background(img_src):
    """
    @return x, y, w, h
    """
    img = img_src.copy()
    h, w = img.shape[:2]
    # 背景填充 进行泛洪填充
    mask = np.zeros((h+2, w+2), np.uint8)  #掩码长和宽都比输入图像多两个像素点，满水填充不会超出掩码的非零边缘 
    cv2.floodFill(img, mask, (5,5), (255,255,255), (3,3,3),(5,5,5),8)

    # 去噪
    img = cv2.fastNlMeansDenoisingColored(img,None,20,20,7,21)

    # 背景识别
    mask=np.zeros((img.shape[:2]),np.uint8)
    bgdModel=np.zeros((1,65),np.float64)
    fgdModel=np.zeros((1,65),np.float64)
    rect=(5,5,w-5,h-5)
    # 多次计算，保证计算准确度
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,2,cv2.GC_INIT_WITH_RECT)
    #关于where函数第一个参数是条件，满足条件的话赋值为0，否则是1。如果只有第一个参数的话返回满足条件元素的坐标。
    mask2=np.where((mask==2)|(mask==0),0,1).astype('uint8')

    # 绘制轮廓
    draw_img=img*mask2[:,:,np.newaxis]
    # 前景图使用白色填充，方便识别
    draw_img[np.where((draw_img > [0,0,0]).all(axis = 2))] =[255,255,255]

    # h, w = draw_img.shape[:2]
    draw_img = cv2.cvtColor(draw_img, cv2.COLOR_BGR2GRAY)  #得到灰度图
    _, binary = cv2.threshold(draw_img,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
    if len(contours) < 1:
        return img
    else:
        max_countor = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        return cv2.boundingRect(max_countor)
