
from GUI_of_Map import Ui_MyMap
from File_list import File_list
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal
from AnimationShadowEffect import AnimationShadowEffect  # @UnresolvedImport
import sys
import os
import threading

video_path="F:\python_programs\大型软件设计/video-for-map"  # where the videos are stored


class Map(Ui_MyMap,QDialog):
    Map_Signal = pyqtSignal(list)


    def __init__(self):
        super(Ui_MyMap, self).__init__()
        self.setupUi(self)
        self.cam_list = [self.cam_17,self.cam_18,self.cam_19,self.cam_20,
                         self.cam_21,self.cam_23,self.cam_24,self.cam_25,
                         self.cam_27,self.cam_28,self.cam_36,self.cam_35]

        self.init_connect()
        self.init_animation()
        self.radius = 20                #The radius of the four corners of the interface
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setStyleSheet("background:url(./Distribution of cameras.jpg)")
        self.cam_selected=None  # the num of the radiobutton clicked




    def init_connect(self):
        for cam in self.cam_list:
            cam.clicked.connect(self.showFiles)

    def init_animation(self):
        for cam in self.cam_list:
            Animation = AnimationShadowEffect(Qt.red, cam)
            cam.setGraphicsEffect(Animation)
            Animation.start()



    def showFiles(self):
        name = self.sender().objectName()         #the name of the radiobutton from which the activating signal was
        print(name)
        self.cam_selected=name[4:]
        videos_list=os.listdir(video_path+"/"+self.cam_selected)
        videos_list.sort()          # make the videos in order

        absolute_path = []
        for video in videos_list:
            absolute_path.append(video_path + "/" + self.cam_selected + "/" + video)
        self.Map_Signal.emit(absolute_path)
        self.close()
        # panel=File_list(videos_list,123)
        # panel.List_Signal.connect(self.get_Signal_from_list)    # the signal from list would activate the func(get_Signal_from_list)
        # panel.exec()


    def get_Signal_from_list(self,connect):
        absolute_path=[]
        for video_selected in connect:
            absolute_path.append(video_path+"/"+self.cam_selected+"/"+video_selected)
        self.Map_Signal.emit(absolute_path)
        self.close()









    def paintEvent(self, event):            #overwrite the paintEvent
        p = QPainter(self)
        p.drawPixmap(QPoint(), self.get_round_pixmap())
        p.drawPixmap(QPoint(self.width() - self.radius, 0), self.get_round_pixmap(True, False))
        p.drawPixmap(QPoint(0, self.height() - self.radius), self.get_round_pixmap(False, True))
        p.drawPixmap(QPoint(self.width() - self.radius, self.height() - self.radius), self.get_round_pixmap(True, True))

    def get_round_pixmap(self, hmirror=False, vmirror=False):
        r = self.radius
        pix = QPixmap(r, r)
        pix.fill(Qt.transparent)
        path = QPainterPath()
        path.moveTo(r, 0)
        path.arcTo(0, 0, r * 2, r * 2, 90, 90)
        path.lineTo(0, 0)
        path.lineTo(r, 0)
        p = QPainter()
        p.begin(pix)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.fillPath(path,Qt.black)
        p.end()
        img = pix.toImage()
        img = img.mirrored(hmirror, vmirror)
        return QPixmap.fromImage(img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyMap=Map()
    MyMap.show()
    sys.exit(app.exec_())