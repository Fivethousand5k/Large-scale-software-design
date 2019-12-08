
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QFile, Qt, QEvent, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QTreeWidgetItem
from PyQt5 import QtCore
from OfflineWindow import OfflineWindow
from visionalgmain import Ui_VisionAlgMain
from utils.util import readBboxFromTxt, draw_bbox,draw_bbox_for_recog,draw_person,is_inside
from config import origin_path,face_mot_switch, person_mot_switch, person_detect_switch,face_recognition_switch,face_recog_txt_path,origin_path,person_detect_txt_path,person_mot_txt_path
from time_shift import time_shift
import datetime
from PyQt5.QtGui import QPixmap
import sys
import cv2
import os
import time
# from segmentation.HumanParsing.seg_offline import OffLineWindow

handling_camera = ['17', '18', '19', '20', '21', '23', '24', '25', '27', '28', '35', '36']

show_person_mot = person_mot_switch
show_person_detect = person_detect_switch
show_face_mot = face_mot_switch
show_face_recog=face_recognition_switch
'''
    主窗口程序  by张精制
'''


class myVideoCapture(cv2.VideoCapture):

    def __init__(self):
        super().__init__()
        self.item = None
        self.window = None
        self.lastVideo = None
        self.detected_txt = None
        self.mot_txt = []
        self.recog_txt=[]
        self.detected_bbox = []
        self.mot_bbox = []
        self.recog_bbox={}
        self.recog_bbox_GroupBy_TrackId={}

class MyMainWindow(QMainWindow, Ui_VisionAlgMain):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.initData()
        self.initVideoLab()
        self.initEvent()
        self.labelIndex = 0

        self.vdo_list=[]
        self.vdo0=myVideoCapture()
        self.vdo1 = myVideoCapture()
        self.vdo2 = myVideoCapture()
        self.vdo3 = myVideoCapture()
        self.vdo4 = myVideoCapture()
        self.vdo5 = myVideoCapture()
        self.vdo6 = myVideoCapture()
        self.vdo7 = myVideoCapture()
        self.vdo8 = myVideoCapture()
        self.vdo9 = myVideoCapture()
        self.vdo10= myVideoCapture()
        self.vdo11= myVideoCapture()
        self.vdo12=myVideoCapture()
        self.vdo13=myVideoCapture()
        self.vdo14 = myVideoCapture()
        self.vdo15 = myVideoCapture()
        
        self.vdo_list=[self.vdo0,self.vdo1,self.vdo2,self.vdo3,self.vdo4,self.vdo5,self.vdo6,self.vdo7,self.vdo8,self.vdo9,self.vdo10,self.vdo11,self.vdo12,self.vdo13,self.vdo14,self.vdo15]
        # for i in range(self.windowNum):
        #     vdo=myVideoCapture()
        #     self.vdo_list.append(vdo)
            
        
        self.timer_list=[]
        # self.timer0 = QTimer(self)
        # self.timer1 = QTimer(self)
        # self.timer2 = QTimer(self)
        # self.timer3 = QTimer(self)
        for i in range(16):
            timer= QTimer(self)
            self.timer_list.append(timer)


    def initUI(self):
        self.move(QPoint(0, 0))
        self.setStyleSheet("QGroupBox#gboxMain{border-width:0px;}")
        file = QFile("client/icons/silvery.qss")
        if file.open(QFile.ReadOnly):
            qss = str(file.readAll(), encoding='utf-8')
            self.setStyleSheet(qss)
            file.close()
        self.setProperty("Form", True)
        self.resize(QSize(1280, 720))
        # self.widget_menu.move(0, 0)
        self.widget_show.move(0, 0)
        # self.widget_menu.setStyleSheet("background-color:#3C3C3C;")
        self.DVRsets_treeView.setHeaderLabels(['ChannelNo', 'Name'])
        self.DVRsets_treeView.setColumnWidth(0, 90)
        self.checkBox_online.setChecked(False)

    def initData(self):
        self.cameraInfo = []  # 摄像头信息  camera.txt配置
        self.VideoLab = []  # 播放label
        self.VideoLay = []  # 播放label布局
        self.tempLab = 0  # 当前选中的label
        self.windowNum = 4  # 屏幕数量
        self.maxWindowNum = 16  # 最多屏幕数量
        self.first_tag=True    #to signify whether the video played is the first one
        self.first_video_id=None
        self.first_video_frame=0
        self.time_benchmark=time_shift[36] #to record the start time of the first , then the video following should apply with the time
        self.timer = []
        for i in range(self.maxWindowNum):
            self.timer.append(QTimer(self))  # 控制播放的QTimer
        self.flush_all = []
        for i in range(self.maxWindowNum):
            self.flush_all.append(False)  # 清空信号初始全为假

        self.capture1 =None
        self.capture2 =None
        self.hog1 = cv2.HOGDescriptor()
        self.hog1.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.hog2 = cv2.HOGDescriptor()
        self.hog2.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


    def initVideoLab(self):
        self.VideoLab.append(self.labVideo1)
        self.VideoLab.append(self.labVideo2)
        self.VideoLab.append(self.labVideo3)
        self.VideoLab.append(self.labVideo4)
        self.VideoLab.append(self.labVideo5)
        self.VideoLab.append(self.labVideo6)
        self.VideoLab.append(self.labVideo7)
        self.VideoLab.append(self.labVideo8)
        self.VideoLab.append(self.labVideo9)
        self.VideoLab.append(self.labVideo10)
        self.VideoLab.append(self.labVideo11)
        self.VideoLab.append(self.labVideo12)
        self.VideoLab.append(self.labVideo13)
        self.VideoLab.append(self.labVideo14)
        self.VideoLab.append(self.labVideo15)
        self.VideoLab.append(self.labVideo16)

        self.VideoLay.append(self.lay1)
        self.VideoLay.append(self.lay2)
        self.VideoLay.append(self.lay3)
        self.VideoLay.append(self.lay4)

        for i in range(16):
            self.VideoLab[i].setProperty("labVideo", True)
            self.VideoLab[i].setText("屏幕{}".format(i + 1))
        self.tempLab = self.VideoLab[0]
        self.show_video_4()  # 初始化时默认显示4个画面

    def change_window_menu(self, pos):  # 处理在视频显示区的右键菜单显示
        menu = QMenu()
        opt1 = menu.addAction("切换到1画面")
        opt2 = menu.addAction("切换到4画面")
        opt3 = menu.addAction("切换到9画面")
        opt4 = menu.addAction("切换到16画面")
        action = menu.exec_(self.gBoxMain.mapToGlobal(pos))
        if action == opt1:
            self.show_video_1()  # 显示1个摄像头
        elif action == opt2:
            self.show_video_4()  # 显示4个摄像头
        elif action == opt3:
            self.show_video_9()  # 显示9个摄像头
        elif action == opt4:
            self.show_video_16()  # 显示16个摄像头
        else:
            return

    def initEvent(self):
        self.btn_login.clicked.connect(self.login)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_offline.clicked.connect(self.offlineHandle)
        # self.btnMenu_PersonParse.clicked.connect(self.parseHandle)
        self.gBoxMain.setContextMenuPolicy(Qt.CustomContextMenu)  # 针对gBoxMain开放右键，gBoxMain是视频显示部分(1,4,9,16)的那部分
        self.gBoxMain.customContextMenuRequested.connect(
            self.change_window_menu)  # 当在gBoxMain区域内点击右键时，调用用户自定义的函数 custom_right_menu
        self.quitoffline = pyqtSignal(object)
        self.checkBox_online.stateChanged.connect(self.clear_all)
        # self.btnMenu_Detect.setMouseTracking(True)
        # self.btnMenu_Detect.installEventFilter(self)
        # self.btnMenu_PersonParse.installEventFilter(self)

        # self.btnMenu_Detect.mouseMoveEvent(event)
        # self.btnMenu_Detect.clicked.connect(self.DetectFuncSelect)

    # def eventFilter(self, object, event):
    #     if event.type() == QEvent.Enter and object == self.btnMenu_Detect:
    #         self.DetectFuncSelect()
    #         # print(object.pos())
    #         # print(self.btnMenu_Detect.pos())
    #         return True
    #     elif event.type() == QEvent.Enter and object.pos() == self.btnMenu_PersonParse.pos():
    #         self.PersonParseFuncSelect()
    #         # print(object.pos())
    #         # print(self.btnMenu_Detect.pos())
    #         return True
    #     elif event.type() == QEvent.Leave:
    #         self.show()
    #     return False

    def parseHandle(self):
        parseWin = OffLineWindow(self.widget_show)
        parseWin.setAttribute(Qt.WA_DeleteOnClose)
        # self.widget_alg.hide()
        # self.widget_main.hide()
        parseWin.show()
        parseWin.move(0, 0)  # 这一行去掉了还能用，搞清楚它是干嘛的


    def login(self):
        self.root = QTreeWidgetItem(self.DVRsets_treeView)
        self.root.setText(0, 'NERCMS')
        self.root.setIcon(0, QIcon("icons/login.bmp"))

        # set child node
        self.parseCameraInfo()
        for i in range(len(self.cameraInfo)):
            child = QTreeWidgetItem(self.root)
            channelNo = self.cameraInfo[i][0]
            child.setText(0, channelNo)
            # name = self.cameraInfo[i][2].strip("\n")
            name = str(i)+"号摄像头"
            child.setText(1, name)
            child.setIcon(0, QIcon("icons/camera.bmp"))
            if handling_camera.__contains__(channelNo):
                child.setBackground(0, QBrush(QColor("#32CD99")))
                child.setBackground(1, QBrush(QColor("#32CD99")))
        self.DVRsets_treeView.addTopLevelItem(self.root)
        self.DVRsets_treeView.expandAll()
        self.DVRsets_treeView.clicked.connect(self.onTreeClick)
        self.DVRsets_treeView.itemDoubleClicked.connect(self.onTreeDoubleClick)

    def onTreeClick(self, index):
        item = self.DVRsets_treeView.currentItem()
        if item.text(0) == 'NERCMS':
            return
        channelNo = int(item.text(0))
        # print(item.text(0), " ", item.text(1))

    def onTreeDoubleClick(self, item):

        Index=self.labelIndex
        if item.text(0) == 'NERCMS':
            return

        if not self.checkBox_online.isChecked():
            channelNo = int(item.text(0))
            video_saved_dir = os.path.join(origin_path, item.text(0))
            detected_result_txt_dir = os.path.join(person_detect_txt_path, item.text(0))
            mot_result_txt_dir = os.path.join(person_mot_txt_path, item.text(0))
            recog_result_txt_dir =os.path.join(face_recog_txt_path,item.text(0))
            videos = os.listdir(detected_result_txt_dir)
            videos = [i for i in videos if i.endswith('.txt')]

            videos = os.listdir(video_saved_dir)
            # videos = [i for i in videos if i.endswith('.txt')]

            if len(videos)==0:
                return
            videos = sorted(videos, reverse=True)
            for i,  _ in enumerate(videos):
                videos[i] = videos[i].replace('txt', 'mp4')
            videos.sort()
            path = os.path.join(video_saved_dir, videos[0]) # show newest video

            self.vdo_list[self.labelIndex].open(path)
            self.vdo_list[self.labelIndex].item = item
            self.vdo_list[self.labelIndex].detected_txt = detected_result_txt_dir
            self.vdo_list[self.labelIndex].mot_txt = mot_result_txt_dir
            self.vdo_list[self.labelIndex].recog_txt = recog_result_txt_dir
            self.vdo_list[self.labelIndex].video_name = videos[0]
            # # self.vdo_list[self.labelIndex].set(cv2.CAP_PROP_POS_FRAMES, 0)
            #
            self.vdo_list[self.labelIndex].detected_bbox = readBboxFromTxt(
                os.path.join(self.vdo_list[self.labelIndex].detected_txt, videos[0]), TaskType='Detection')
            # self.vdo_list[self.labelIndex].mot_bbox = readBboxFromTxt(
            #     os.path.join(self.vdo_list[self.labelIndex].mot_txt, videos[0]), TaskType='MOT')
            # self.vdo_list[self.labelIndex].recog_bbox = readBboxFromTxt(
            #     os.path.join(self.vdo_list[self.labelIndex].recog_txt, videos[0]),result_GroupBy_trackid=
            #     self.vdo_list[self.labelIndex].recog_bbox_GroupBy_TrackId, TaskType='RECOG')
            # if self.first_tag:  # if this is the first video being played
            #     is_first_flag = True
            #     id = int(item.text(0))
            #     self.first_video_id = Index
            #     start_time=time_shift[id]
            #     delta_time=(self.time_benchmark-start_time).seconds
            #     self.first_video_frame_shift=delta_frame=int(delta_time/0.05)
            #     if delta_time !=0:
            #         self.vdo_list[Index].set(cv2.CAP_PROP_POS_FRAMES, delta_frame)  # 设置从哪一帧开始播放视�?
            #     self.first_tag=False
            # else:
            #     is_first_flag = False
            #     id = int(item.text(0))
            #     delta_time =(self.time_benchmark-time_shift[id]).seconds
            #     delta_frame=delta_time/0.05+self.first_video_frame-self.first_video_frame_shift
            #     self.vdo_list[Index].set(cv2.CAP_PROP_POS_FRAMES, delta_frame)
            if self.flush_all[self.labelIndex]:
                self.flush_all[self.labelIndex]=False
            self.timer_list[self.labelIndex].timeout.connect(lambda: self.play_offline(Index=Index,is_first_flag=False))
            self.timer_list[self.labelIndex].start(45)
            self.vdo_list[self.labelIndex].lastVideo = videos[0]
            print(channelNo)


        else:    #online processing
            if self.flush_all[self.labelIndex]:
                self.flush_all[self.labelIndex] = False
            video1 = "http://admin:admin@192.168.43.99:8081/"  # 此处@后的ipv4 地址需要修改为自己的地址
            # video2 = "http://admin:admin@192.168.43.224:8081/"  # 此处@后的ipv4 地址需要修改为自己的地址
            self.capture1 = cv2.VideoCapture(video1)
            # self.capture2 = cv2.VideoCapture(video2)
            self.timer_list[self.labelIndex].timeout.connect(
                lambda: self.play_online(Index=Index))
            self.timer_list[self.labelIndex].start(20)


        self.labelIndex += 1
        self.labelIndex %= 16


    def logout(self):    # def onTreeDoubleClick(self, item):
    #
    #     if item.text(0) == 'NERCMS':
    #         return
    #     channelNo = int(item.text(0))
    #     video_saved_dir = os.path.join("/home/mmap/vsa_server/camera/origin/", item.text(0))
    #     detected_result_txt_dir = os.path.join("/home/mmap/vsa_server/camera/txt_results/person_detect/", item.text(0))
    #     mot_result_txt_dir = os.path.join("/home/mmap/vsa_server/camera/txt_results/person_mot/", item.text(0))
    #     recog_result_txt_dir = os.path.join(face_recog_txt_path, item.text(0))
    #     videos = os.listdir(detected_result_txt_dir)
    #     videos = [i for i in videos if i.endswith('.txt')]
    #
    #     if len(videos) == 0:
    #         return
    #     videos = sorted(videos, reverse=True)
    #     for i, _ in enumerate(videos):
    #         videos[i] = videos[i].replace('txt', 'mp4')
    #     videos.sort()
    #     path = os.path.join(video_saved_dir, videos[0])  # show newest video
    #
    #     self.vdo_list[self.labelIndex].open(path)
    #     self.vdo_list[self.labelIndex].item = item
    #     self.vdo_list[self.labelIndex].detected_txt = detected_result_txt_dir
    #     self.vdo_list[self.labelIndex].mot_txt = mot_result_txt_dir
    #     self.vdo_list[self.labelIndex].recog_txt = recog_result_txt_dir
    #     self.vdo_list[self.labelIndex].video_name = videos[0]
    #     # self.vdo_list[self.labelIndex].set(cv2.CAP_PROP_POS_FRAMES, 0)
    #
    #     self.vdo_list[self.labelIndex].detected_bbox = readBboxFromTxt(
    #         os.path.join(self.vdo_list[self.labelIndex].detected_txt, videos[0]), TaskType='Detection')
    #     self.vdo_list[self.labelIndex].mot_bbox = readBboxFromTxt(
    #         os.path.join(self.vdo_list[self.labelIndex].mot_txt, videos[0]), TaskType='MOT')
    #     self.vdo_list[self.labelIndex].recog_bbox = readBboxFromTxt(
    #         os.path.join(self.vdo_list[self.labelIndex].recog_txt, videos[0]), result_GroupBy_trackid=
    #         self.vdo_list[self.labelIndex].recog_bbox_GroupBy_TrackId, TaskType='RECOG')
    #
    #     Index = self.labelIndex
    #     if self.first_tag:  # if this is the first video being played
    #         is_first_flag = True
    #         id = int(item.text(0))
    #         self.first_video_id = Index
    #         start_time = time_shift[id]
    #         delta_time = (self.time_benchmark - start_time).seconds
    #         self.first_video_frame_shift = delta_frame = int(delta_time / 0.05)
    #         if delta_time != 0:
    #             self.vdo_list[Index].set(cv2.CAP_PROP_POS_FRAMES, delta_frame)  # 设置从哪一帧开始播放视�?
    #         self.first_tag = False
    #     else:
    #         is_first_flag = False
    #         id = int(item.text(0))
    #         delta_time = (self.time_benchmark - time_shift[id]).seconds
    #         delta_frame = delta_time / 0.05 + self.first_video_frame - self.first_video_frame_shift
    #         self.vdo_list[Index].set(cv2.CAP_PROP_POS_FRAMES, delta_frame)
    #
    #     self.timer_list[self.labelIndex].timeout.connect(lambda: self.play(Index=Index, is_first_flag=is_first_flag))
    #     self.timer_list[self.labelIndex].start(50)
    #     self.vdo_list[self.labelIndex].lastVideo = videos[0]
    #
    #     self.labelIndex += 1
    #     self.labelIndex %= 16
    #     print(channelNo)
    #
        self.DVRsets_treeView.clear()
        self.cameraInfo.clear()


    def play_online(self,Index):

        if Index % 2 == 0:
            success, img = self.capture1.read()
        else:
            success, img = self.capture2.read()
        if success:
            if self.checkBox_HumanDetection.isChecked():        #need person detection
                if Index%2==0:
                    found, w = self.hog1.detectMultiScale(img)
                else:
                    found, w = self.hog2.detectMultiScale(img)

                foundList = []
                for ri, r in enumerate(found):
                    flag = 0
                    for qi, q in enumerate(found):
                        if ri != qi and is_inside(r, q):
                            flag = 1
                    if (flag == 0):
                        foundList.append(r)
                for person in foundList:
                    draw_person(img, person)


            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(img,
                               (int(self.VideoLab[Index].width() * 0.98), int(self.VideoLab[Index].height() * 0.98)),
                               interpolation=cv2.INTER_AREA)
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            qimg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            qimg = QtGui.QPixmap.fromImage(qimg)
            self.VideoLab[Index].setPixmap(qimg)



        if self.flush_all[Index]:               #如果检测到清空信号为真
            self.flush_all[Index] = False  # 清空后自动重置信号
            self.timer_list[Index].disconnect()
            self.VideoLab[Index].setPixmap(QPixmap(""))
            if self.labelIndex!=0:
                self.labelIndex-=1



    def play_offline(self,Index,is_first_flag):


        frame_id = int(self.vdo_list[Index].get(1))
        if is_first_flag:
            self.first_video_frame=frame_id

        ret, frame = self.vdo_list[Index].read()

        detected_bboxes = []
        mot_bboxes = []
        recog_bboxes=[]
        if frame_id in self.vdo_list[Index].detected_bbox:
            detected_bboxes = self.vdo_list[Index].detected_bbox[frame_id]
        if frame_id in self.vdo_list[Index].mot_bbox:
            mot_bboxes = self.vdo_list[Index].mot_bbox[frame_id]
        if frame_id in self.vdo_list[Index].recog_bbox:
            recog_bboxes = self.vdo_list[Index].recog_bbox[frame_id]



        if ret:
            # if show_person_detect == True:
            if self.checkBox_HumanDetection.isChecked():
                for box in detected_bboxes:
                    frame = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 5)
            if show_person_mot == True:
                for box in mot_bboxes:
                    frame = draw_bbox(frame, box[0:4], box[-1])
            if show_face_recog == True:
                frame = draw_bbox_for_recog(frame,
                                            recog_bboxes,self.windowNum,self.vdo_list[Index].recog_bbox_GroupBy_TrackId)  # draw all the boxes at a time rather than draw a box one by one

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame,(int(self.VideoLab[Index].width()*0.98),int(self.VideoLab[Index].height()*0.98)),interpolation=cv2.INTER_AREA)
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qimg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            qimg = QtGui.QPixmap.fromImage(qimg)
            # print("play", str(Index))
            # if Index is 0:
            #     self.VideoLab[0].setPixmap(qimg)
            #     self.VideoLab[0].setScaledContents(True)
            # elif Index is 1:
            #     self.VideoLab[1].setPixmap(qimg)
            #     self.VideoLab[1].setScaledContents(True)

            # self.VideoLab[Index].setScaledContents(True)
            self.VideoLab[Index].setPixmap(qimg)

            # self.VideoLab[1].setPixmap(qimg)
            # self.VideoLab[1].setScaledContents(True)

        else:
            # self.playnext(self.vdo_list[Index],Index)
            self.timer_list[Index].disconnect()
            self.VideoLab[Index].setPixmap(QPixmap(""))


        if self.flush_all[Index]:               #如果检测到清空信号为真
            self.flush_all[Index] = False  # 清空后自动重置信号
            self.timer_list[Index].disconnect()
            self.VideoLab[Index].setPixmap(QPixmap(""))
            if self.labelIndex!=0:
                self.labelIndex-=1




    def playnext(self, videocap,Index):

        item = videocap.item

        video_saved_dir = os.path.join(origin_path, item.text(0))
        # video_saved_dir = os.path.join("/home/mmap/vsa_server/camera/origin/", item.text(0))
        # detected_result_txt_dir = os.path.join("/home/mmap/vsa_server/camera/txt_results/person_detect/", item.text(0))
        # mot_result_txt_dir = os.path.join("/home/mmap/vsa_server/camera/txt_results/person_mot/", item.text(0))
        # recog_result_txt_dir = os.path.join(face_recog_txt_path, item.text(0))
        # videos = os.listdir(detected_result_txt_dir)
        # videos = [i for i in videos if i.endswith('.txt')]
        videos = os.listdir(origin_path)

        if len(videos) == 0:
            return

        videos = sorted(videos, reverse=True)

        for i, _ in enumerate(videos):
            videos[i] = videos[i].replace('txt', 'mp4')

        path = os.path.join(video_saved_dir, videos[0])

        videocap.lastVideo = videos[0]

        # videocap.detected_txt = detected_result_txt_dir
        # videocap.mot_txt = mot_result_txt_dir
        # videocap.recog_txt =recog_result_txt_dir
        videocap.video_name = videos[0]

        # videocap.detected_bbox = readBboxFromTxt(os.path.join(videocap.detected_txt, videos[0]), TaskType='Detection')
        #
        # videocap.mot_bbox = readBboxFromTxt(os.path.join(videocap.mot_txt, videos[0]), TaskType='MOT')
        # videocap.recog_bbox =readBboxFromTxt(os.path.join(videocap.recog_txt, videos[0]), TaskType='RECOG',result_GroupBy_trackid=self.vdo_list[Index].recog_bbox_GroupBy_TrackId)
        #

        videocap.open(path)
        print(videos)

    def parseCameraInfo(self):
        with open("client/ini/camera.txt", errors='ignore') as f:
            for line in f:
                info = line.split(' ')
                self.cameraInfo.append(info)

    def offlineHandle(self):
        self.timer0.disconnect()
        self.timer1.disconnect()
        self.timer2.disconnect()
        self.timer3.disconnect()
        self.myOffline = OfflineWindow(self.widget_show)
        self.myOffline.setAttribute(Qt.WA_DeleteOnClose)
        self.widget_alg.hide()  # 这一行去掉了还能用，搞清楚它是干嘛的
        self.widget_main.hide()  # 这一行去掉了还能用，搞清楚它是干嘛的
        self.myOffline.show()
        self.myOffline.move(0, 0)  # 这一行去掉了还能用，搞清楚它是干嘛的

    def removeLayout(self):
        for i in range(4):
            self.VideoLay[0].removeWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(False)

        for i in range(4, 8):
            self.VideoLay[1].removeWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(False)

        for i in range(8, 12):
            self.VideoLay[2].removeWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(False)

        for i in range(12, 16):
            self.VideoLay[3].removeWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(False)

    def show_video_1(self):  # 显示1个摄像头
        self.removeLayout()
        self.windowNum = 1
        self.video_max = True
        self.change_video_1()

    def change_video_1(self, index=0):
        for i in range((index + 0), (index + 1)):
            self.VideoLay[0].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)

    def show_video_4(self):  # 显示4个摄像头
        self.removeLayout()
        self.windowNum = 4
        self.video_max = False
        self.change_video_4()

    def change_video_4(self, index=0):
        for i in range((index + 0), (index + 2)):
            self.VideoLay[0].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)
        for i in range((index + 2), (index + 4)):
            self.VideoLay[1].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)

    def show_video_9(self):  # 显示9个摄像头
        self.removeLayout()
        self.windowNum = 9
        self.video_max = False
        self.change_video_9()

    def change_video_9(self, index=0):
        for i in range((index + 0), (index + 3)):
            self.VideoLay[0].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)
        for i in range((index + 3), (index + 6)):
            self.VideoLay[1].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)
        for i in range((index + 6), (index + 9)):
            self.VideoLay[2].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)

    def show_video_16(self):  # 显示16个摄像头
        self.removeLayout()
        self.windowNum = 16
        self.video_max = False
        self.change_video_16()

    def change_video_16(self, index=0):
        for i in range((index + 0), (index + 4)):
            self.VideoLay[0].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)
        for i in range((index + 4), (index + 8)):
            self.VideoLay[1].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)
        for i in range((index + 8), (index + 12)):
            self.VideoLay[2].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)
        for i in range((index + 12), (index + 16)):
            self.VideoLay[3].addWidget(self.VideoLab[i])
            self.VideoLab[i].setVisible(True)

    def DetectFuncSelect(self):

        menu = QMenu()
        opt1 = menu.addAction("算法A")
        opt2 = menu.addAction("算法B")

        position = QPoint(self.btnMenu_Detect.geometry().x() + self.btnMenu_Detect.geometry().height() + self.pos().x(),
                          self.btnMenu_Detect.geometry().y() + self.btnMenu_Detect.geometry().width() / 2 + self.pos().y())
        action = menu.exec_(position)
        if action == opt1:
            self.algorithmA()
        elif action == opt2:
            self.algorithmB()

        else:
            return

    def PersonParseFuncSelect(self):

        menu = QMenu()
        opt1 = menu.addAction("算法A")
        opt2 = menu.addAction("算法B")

        position = QPoint(
            self.btnMenu_PersonParse.geometry().x() + self.btnMenu_PersonParse.geometry().height() + self.pos().x(),
            self.btnMenu_PersonParse.geometry().y() + self.btnMenu_PersonParse.geometry().width() / 2 + self.pos().y())
        action = menu.exec_(position)
        if action == opt1:
            self.algorithmA()
        elif action == opt2:
            self.algorithmB()

        else:
            return

    def algorithmA(self):
        print("AAAAAAAAAA")

    def algorithmB(self):
        print("BBBBBBBBBB")

    def clear_all(self):

        print("clear-all!")
        for i in range(self.maxWindowNum):
            self.flush_all[i]=True
        self.labelIndex=0





if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icons/v.ico'))
    myWin = MyMainWindow()
    myWin.setWindowFlags(Qt.Window)
    # myWin.onTreeDoubleClick('19')
    myWin.show()
    # print(myWin.mapToGlobal())
    sys.exit(app.exec_())
