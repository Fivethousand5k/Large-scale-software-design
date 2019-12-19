"""
By Fivethousand
"""
import threading

from GUI_For_Processor import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QFile, Qt, QEvent, QPoint, QTimer,QRect
from PyQt5.QtGui import QIcon, QBrush, QColor, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QTreeWidgetItem, QLabel, QGridLayout, QPushButton, \
    QFileDialog
import copy
import cv2
import numpy as np
from functools import partial
import sys
import os




MAXSIZE=300      #用于图片label最大能支持的分辨率，大于这个值的图像进行等比例放缩，小于这个值的图像加黑边
COLOR='red'         #'blue' or 'green'






class ImageProcessor(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.setupUi(self)
        self.init_connect()
        self.init_gui()
        self.init_mutex()
        self.init_data()

    def init_data(self):
        self.filename=None
        self.raw_image=None

    def init_connect(self):
        self.BTN_Open.clicked.connect(self.HandleOpen)
        self.BTN_ShutOpen.clicked.connect(self.HandleShutOpen)
        self.Slider_Min.sliderReleased.connect(lambda:self.HandleSliderRelease(self.Slider_Min))
        self.Slider_Max.sliderReleased.connect(lambda:self.HandleSliderRelease(self.Slider_Max))
        self.Slider_Min.valueChanged.connect(lambda:self.Handle_Changing_slider(self.Slider_Min))
        self.Slider_Max.valueChanged.connect(lambda: self.Handle_Changing_slider(self.Slider_Max))
        self.ComboBox.activated.connect(self.set_Min_And_Max)       #调整滑条的最大值和最小值，并触发图片处理

    def init_gui(self):
        self.Slider_Min.setMinimum(0)
        self.Slider_Min.setMaximum(255) 
        self.Slider_Min.setSingleStep(1)
        self.Slider_Max.setMinimum(0)
        self.Slider_Max.setMaximum(255)
        self.Slider_Max.setSingleStep(1)
        self.treeWidget.headerItem().setText(0, "文件列表")

    def init_mutex(self):
        self.mutex1 = threading.Lock()

    def HandleOpen(self):
        """        这个是打开单张图片的版本
        imgPath, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        if imgPath:     # if imgPath is not empty
            self.raw_image=imgPath
            self.Show_RawImage()

            f = open('./RecentOpen.txt', 'a+')      #change the path recently opened
            f.seek(0)
            f.truncate()  # 清空文件
            f.write(imgPath)              # and write a new one
            f.close()
        else:
            print("the imgPath is empty!!!!!")
        """

        self.filename = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        if self.filename:  # if self.filename is not empty
            f = open('./RecentOpen_forProcessor.txt', 'a+')  # change the path recently opened
            f.seek(0)
            f.truncate()  # 清空文件
            f.write(self.filename)  # and write a new one
            f.close()
            file_list = os.listdir(self.filename)
            file_list.sort()
            root = QTreeWidgetItem(self.treeWidget)
            root.setText(0, self.filename)
            for file in file_list:
                child1=QTreeWidgetItem(root)
                child1.setText(0,file)
            self.treeWidget.addTopLevelItem(root)
            self.treeWidget.clicked.connect(self.HandleImageClicked)
        else:
            print("the Path is empty!!!!!")


    def HandleShutOpen(self):
        """ 这个是打开单张图片的版本
        # f = open('./RecentOpen.txt', 'r+')
        # read_data = f.read()
        # f.close()
        # self.raw_image = read_data
        # self.Show_RawImage()
        """
        #打开文件夹版本
        f = open('./RecentOpen_forProcessor.txt', 'r+')
        read_data = f.read()
        f.close()
        if read_data:   # if read_data is not empty
            self.filename=read_data
            file_list = os.listdir(self.filename)
            file_list.sort()
            root = QTreeWidgetItem(self.treeWidget)
            root.setText(0, self.filename)
            for file in file_list:
                child1 = QTreeWidgetItem(root)
                child1.setText(0, file)
            self.treeWidget.addTopLevelItem(root)
            self.treeWidget.clicked.connect(self.HandleImageClicked)
        else:
            print("the txt is empty!")




    def Show_RawImage(self):            # show the raw image in the left label
        img = cv2.imread(self.raw_image)  # convert raw_image into matrix
        RGB_img=img
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB
        RGB_img=self.adjust_size(RGB_img)
        height, width, channel = RGB_img.shape
        bytesPerLine = 3 * width
        showImage = QImage(RGB_img, width, height, bytesPerLine,
                           QImage.Format_RGB888)  # 转换成QImage类型
        self.lbl_RawImage.setScaledContents(True)
        self.lbl_RawImage.setPixmap(QPixmap.fromImage(showImage))  # 图像输出至label


    def img_process(self):
        img=cv2.imread(self.raw_image)  #convert raw_image into matrix
        RGB_img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB



        RGB_img=self.draw_pixel(self.Slider_Min.value(),self.Slider_Max.value(),RGB_img,COLOR)

        RGB_img=self.adjust_size(RGB_img)   #调整尺寸，变成MAXSIZE*MAXSIZE

        height, width, channel = RGB_img.shape
        bytesPerLine = 3 * width
        showImage = QImage(RGB_img, width, height, bytesPerLine,
                           QImage.Format_RGB888)  # 转换成QImage类型
        self.lbl_ProcessedImage.setScaledContents(True)
        self.lbl_ProcessedImage.setPixmap(QPixmap.fromImage(showImage))  # 图像输出至label





    def draw_pixel(self,min,max,RGB_img,color='red'):              #将图像中约束条件处于[min，max]之间的像素点绘制成某种颜色
        """

        :param min:  约束条件最小值
        :param max:  约束条件最大值
        :param RGB_img: 待处理图像的RGB矩阵
        :param color:   将满足要求的像素点转换成的颜色，默认为红色
        :return:    处理后的RGB矩阵
        """
        handle_list=[]              #用于保存需要处理的像素点的位置

        if self.ComboBox.currentText()=='像素值':
            gray_img = cv2.cvtColor(RGB_img, cv2.COLOR_RGB2GRAY)  # 转换为灰度图、
            max_matrix=np.array(gray_img <=max, dtype='int')            #提取灰度矩阵中小于等于max的部分，标志位为1
            min_matrix=np.array(gray_img >=min, dtype='int')            #提取灰度矩阵中大于等于min的部分，标志位为1
            tag_matrix = max_matrix & min_matrix                        #得到既小于等于max又大于等于min的部分，标志位为1


        elif self.ComboBox.currentText()=='梯度':
            """
            增加梯度功能时，也需要计算出tag_matrix，即需要处理的像素点的标志位，传入pixel_dyer中
            """
            pass

        else:
            print("暂不支持此功能！")
            pass

        self.pixel_dyer(RGB_img, tag_matrix, color)
        return RGB_img

    def pixel_dyer(self,RGB_img,tag_matrix,color):
        Not_tag_matrix = -(tag_matrix - np.ones(tag_matrix.shape))  # tag_matrix中0-1互换
        if color == 'red':
            RGB_img[:, :, 0] = np.multiply(Not_tag_matrix, RGB_img[:, :, 0])  # 按位相乘
            RGB_img[:, :, 0] = RGB_img[:, :, 0] + 128 * tag_matrix  # R通道置128
            RGB_img[:, :, 1] = np.multiply(Not_tag_matrix, RGB_img[:, :, 1])
            RGB_img[:, :, 2] = np.multiply(Not_tag_matrix, RGB_img[:, :, 2])
        elif color == 'green':
            RGB_img[:, :, 1] = np.multiply(Not_tag_matrix, RGB_img[:, :, 0])  # 按位相乘
            RGB_img[:, :, 1] = RGB_img[:, :, 0] + 128 * tag_matrix  # G通道置128
            RGB_img[:, :, 0] = np.multiply(Not_tag_matrix, RGB_img[:, :, 1])
            RGB_img[:, :, 2] = np.multiply(Not_tag_matrix, RGB_img[:, :, 2])
        elif color == 'blue':
            RGB_img[:, :, 2] = np.multiply(Not_tag_matrix, RGB_img[:, :, 0])  # 按位相乘
            RGB_img[:, :, 2] = RGB_img[:, :, 0] + 128 * tag_matrix  # B通道置128
            RGB_img[:, :, 0] = np.multiply(Not_tag_matrix, RGB_img[:, :, 1])
            RGB_img[:, :, 1] = np.multiply(Not_tag_matrix, RGB_img[:, :, 2])





    def HandleSliderRelease(self,slider):
            if slider == self.Slider_Min:
                if self.Slider_Min.value()>self.Slider_Max.value():
                    self.Slider_Max.setValue(self.Slider_Min.value())
            elif slider == self.Slider_Max:
                if self.Slider_Min.value()>self.Slider_Max.value():
                    self.Slider_Min.setValue(self.Slider_Max.value())

            if self.raw_image is not None:
                self.img_process()


    def Handle_Changing_slider(self, slider):
            if slider == self.Slider_Min:
                self.lbl_Min.setText(str(self.Slider_Min.value()))
            elif slider == self.Slider_Max:
                self.lbl_Max.setText(str(self.Slider_Max.value()))

    def HandleImageClicked(self):
        item = self.treeWidget.currentItem()
        if item.childCount() is  0 and item.parent() is not None:       #保证只有一级子节点才响应点击
            self.raw_image = os.path.join(self.filename, item.text(0))
            self.set_Min_And_Max()
            self.Show_RawImage()

    def adjust_size(self,RGB_img):
        """
        功能：为了保证图像不形变，适应label的拉伸，而给小图像增加黑边或者对大图像进行等比例放缩
        :param RGB_img:   传入的RGB矩阵
        :return:
        """

        #
        height, width, channel = RGB_img.shape
        if height<=MAXSIZE and width<=MAXSIZE:              #如果图片未超过最大尺寸
            background =np.zeros([MAXSIZE,MAXSIZE,channel],np.uint8)  # 制作一个黑色底片
            top_indent=int((MAXSIZE-height)/2)      #上方间隙
            left_indent=int((MAXSIZE-width)/2 )      #侧方间隙
            background[top_indent:(top_indent+height),left_indent:(left_indent+width),:]=RGB_img[:,:,:]
            return background
        else:                       #图片超过最大尺寸
            """
            
            这一段是在网上找的代码，以后再看，参考链接：https://blog.csdn.net/zhou4411781/article/details/95449322
            
            """
            size = RGB_img.shape
            h, w = size[0], size[1]
            # 长边缩放为MAXSIZE
            scale = max(w, h) / float(MAXSIZE)
            new_w, new_h = int(w / scale), int(h / scale)
            resize_RGB_img = cv2.resize(RGB_img, (new_w, new_h))
            # 填充至MAXSIZE * MAXSIZE
            if new_w % 2 != 0 and new_h % 2 == 0:
                top, bottom, left, right = (MAXSIZE - new_h) / 2, (MAXSIZE - new_h) / 2, (MAXSIZE - new_w) / 2 + 1, (
                        MAXSIZE - new_w) / 2
            elif new_h % 2 != 0 and new_w % 2 == 0:
                top, bottom, left, right = (MAXSIZE - new_h) / 2 + 1, (MAXSIZE - new_h) / 2, (MAXSIZE - new_w) / 2, (
                        MAXSIZE - new_w) / 2
            elif new_h % 2 == 0 and new_w % 2 == 0:
                top, bottom, left, right = (MAXSIZE - new_h) / 2, (MAXSIZE - new_h) / 2, (MAXSIZE - new_w) / 2, (
                        MAXSIZE - new_w) / 2
            else:
                top, bottom, left, right = (MAXSIZE - new_h) / 2 + 1, (MAXSIZE - new_h) / 2, (
                        MAXSIZE - new_w) / 2 + 1, (MAXSIZE - new_w) / 2
            pad_img = cv2.copyMakeBorder(resize_RGB_img, int(top), int(bottom), int(left), int(right), cv2.BORDER_CONSTANT,
                                         value=[0, 0, 0])  # 从图像边界向上,下,左,右扩的像素数目
            return pad_img

    def set_Min_And_Max(self):          #调整滑条的最大值和最小值，并触发图片处理
        if self.raw_image is not None:      #当用户已经选择了待处理图片
            if self.ComboBox.currentText()=='像素值':
                img = cv2.imread(self.raw_image)  # convert raw_image into matrix

                Min,Max=np.min(img),np.max(img)
                print(Min,Max)
                self.Slider_Min.setMinimum(Min)
                self.Slider_Min.setMaximum(Max)
                self.Slider_Max.setMinimum(Min)
                self.Slider_Max.setMaximum(Max)
            elif self.ComboBox.currentText()=='梯度':
                pass

            # self.img_process()

















if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = ImageProcessor()
    myWin.setWindowFlags(Qt.Window)
    myWin.show()
    sys.exit(app.exec_())