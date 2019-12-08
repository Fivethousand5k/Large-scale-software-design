# 界面文件为 FirstMainWin.py
import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QFile, Qt, QEvent, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QFrame, QFileDialog, QWidget
import sys

# 继承至界面文件的主窗口类


from offline import Ui_offline



class OfflineWindow(QMainWindow, Ui_offline):
    def __init__(self, parent=None):
        super(OfflineWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.initEvent()
        self.timer = QTimer(self)
        self.isPlay = False
        self.frameIndex = 0
        self.output_path = '/home/mmap/work/VSA_Client/sequences/zjz/'

    def initUI(self):
        self.setStyleSheet("QGroupBox#gboxMain{border-width:0px;}")
        self.setProperty("Form", True)
        self.setWindowFlags(Qt.Widget)
        self.setWindowTitle("本地视频文件处理")
        self.widget_alg.move(0, 0)
        self.widge_title.move(0, 40)
        self.widget_main.move(0, 70)
        self.play_show.setText("")
        self.play_show.setFrameShape(QFrame.Box)
        self.play_show.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(128,128,128);")

        self.play_show2.setText("")
        self.play_show2.setFrameShape(QFrame.Box)
        self.play_show2.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(128,128,128);")
        # str_bg = ["背景建模", "KNN", "MOG2"]
        # self.addCboxItem(self.cbox_bg, str_bg)
        # str_od = ["行人检测", "YOLOV3_tiny", "YOLOV3"]
        # self.addCboxItem(self.cbox_od, str_od)
        # str_sot = ["单目标跟踪", "SiamFC", "SiamRPN", "SiamRPN-CIR"]
        # self.addCboxItem(self.cbox_sot, str_sot)
        # str_mot = ["多目标跟踪", "DeepSort"]
        # self.addCboxItem(self.cbox_mot, str_mot)
    def initEvent(self):
        self.btn_back2online.clicked.connect(self.back2onlineHandle)                        #点击了"返回在线处理"按钮，则执行back2onlineHandle函数
        self.btn_open.clicked.connect(self.open_query_video)
        self.btn_play.clicked.connect(self.label_click)



    def addCboxItem(self, target, items):
        for i in range(len(items)):
            target.addItem(items[i])

    def back2onlineHandle(self):
        pass
        # self.myMain=MyMainWindow(self.widget_show)
        # self.myMain.setAttribute(Qt.WA_DeleteOnClose)
        # self.myMain.show()
        # self.myOffline.move(0, 0)
        # self.myOffline = OfflineWindow(self.widget_show)
        # self.myOffline.setAttribute(Qt.WA_DeleteOnClose)
        # self.widget_alg.hide()  # 这一行去掉了还能用，搞清楚它是干嘛的
        # self.widget_main.hide()  # 这一行去掉了还能用，搞清楚它是干嘛的
        # self.myOffline.show()
        # self.myOffline.move(0, 0)  # 这一行去掉了还能用，搞清楚它是干嘛的

    def open_query_video(self):
        self.query_video, fileType = QFileDialog.getOpenFileName(self, 'Open a query video', './source',
                                                                 '*.mp4;;*.avi;;All Files(*)')
        self.vdo = cv2.VideoCapture(self.query_video)
        self.isPlay = True
        self.btn_play.setText("暂停")
        self.timer.timeout.connect(self.play)
        self.timer.start(50)

    def play(self):
        ret, frame = self.vdo.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (850, 480))
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qimg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            qimg = QtGui.QPixmap.fromImage(qimg)
            self.play_show.setPixmap(qimg)
            self.play_show.setScaledContents(True)
            self.frameIndex += 1
        else:
            self.timer.disconnect()


    def playFrame(self):
        frame_index = '%04d' % self.frameIndex
        frame_path = self.output_path + frame_index + '.jpg'
        frame = cv2.imread(frame_path)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (850, 480))
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qimg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        qimg = QtGui.QPixmap.fromImage(qimg)
        self.play_show2.setPixmap(qimg)
        self.play_show2.setScaledContents(True)
        self.frameIndex += 1


    def label_click(self):
        if self.isPlay == True:
            self.btn_play.setText("播放")
            self.timer.disconnect()
            self.isPlay = False
        else:
            self.btn_play.setText("暂停")
            self.isPlay = True
            self.play_show.hide()
            self.play_show2.show()
            self.timer.timeout.connect(self.playFrame)
            self.timer.start()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setWindowIcon(QIcon('icons/v.ico'))
#     myWin = OfflineWindow()
#     myWin.setWindowFlags(Qt.Window)
#     myWin.show()
#     sys.exit(app.exec_())
