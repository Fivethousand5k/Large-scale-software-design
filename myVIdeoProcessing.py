#coding:utf-8
# by Fivethousand

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PIL import Image
from PIL import ImageFont, ImageDraw
import threading
from PyQt5.QtCore import QTimer,Qt,QEvent
import cv2
import time
import numpy as np
from GUI import Ui_MainWindow
from MAP import Map
from MyColor import MyColor
from AnimationShadowEffect import AnimationShadowEffect
import sys
import pickle
import os

# sys.path.append('../')
# from facedetect.mtcnn.detector import MTCNNFaceDetector as detector
# from feature.face.faceExtractor import FaceExtractor as faceExtractor
# from mot.deepsort.face_deep_sort import FaceDeepSort as DeepSort
# from utils import convert_to_square

# import freetype


txt_root_path="F:\python_programs\大型软件设计/txt-results"

name_list=['周建力', '姜龙祥', '张精制', '方寒', '柴笑宇', '沈宇轩', 'unknown', '阮威健', '虞吟雪', '郑淇', 'unknown', '陈金', '胡亮', '彭冬梅', '1', '1', '徐东曙', '廖良', '陈俊奎', '洪琪', '高熙越', '黄志兵', '张莎莎', '1', '高腾飞', '陈超', '1', '叶钰', '2', '许海燕', '朱玟谦', '汤云波', '江奎', '1', '丁新', '1', '王旭', '杨光耀', '刘旷也', '1', '王晓芬', '张垒', '郭进', '陈宇静', '胡梦顺', '张钰慧', '梁超', '王南西', '陈宇', '陈军', 'unknown', 'unknown', '2', '刘勇琰', '1', '兰佳梅', 'unknown', '黄鹏', '沈心怡', '陈思维', '陈保金', '王光成', '詹泽行', '赵海法', '焦黎', '胡必成', '孙志宏', '王松', '1', '1', '1', '万东帅', '1', '里想', '1', '陈丹', '1', '魏明高', '聂伟凡', '屈万倩', '柯亨进', '1', '2', '陈培璐', '', '1', '1', '李希希', '易敏', '张琪', '1', '刘晗', '1', '1', '白云鹏', '1', '1', '阮威健', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '黄文心', '1', '1', '1', '1', '1', '1', '1','1','1','1','1','1']

for i in range(len(name_list)):
    if name_list[i]=='1':
        name_list[i]=str(i)
name_list[100]='5000'


video_test=['F:\python_programs/video-for-map/36/new-treasure-island.mp4']

class myVideoProcessing(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.init_data()
        self.init_mutex()
        self.init_connect()
        self.init_GuiSettings()

    def init_data(self):  # 初始化数�?
        self.videoCap =None             #cv2.VideoCapture("./record.mp4")
        self.data = np.loadtxt("./Characteristics/info.txt")  # 将文件中数据加载到data数组�?
        # self.frameToStart = self.data[0][0]  # 从轨迹txt中最小的帧开�?节约时间                             （实时系统不再需要）
        self.playable = True  # 用于控制视频的播放和暂停
        self.count = 0  #每一个视频都从头开始播放，用于记录当前视频读到了哪一�?
        # self.count_TxtLine = 0  # 记录txt读到了哪一�?            (实时系统不再需要）
        # self.videoCap.set(cv2.CAP_PROP_POS_FRAMES, self.frameToStart)  # 设置从哪一帧开始播放视�?            (实时系统不再需要）
        self.traits = {}  # 用于保留轨迹信息的字�?
        self.historic_max_pre = {}  # 用于保存最大历史判定信息的字典(�?-update_limit的范围内作比较）
        self.interval = 0  # 帧与帧之间的处理时间间隔,注意！单位是毫秒�?
        self.update_limit = 15
        self.judge_threshold = 0.0
        self.pred_threshold = 0  # 用于func1 函数，当分数值大于它时，才会在图像上显示人名，否则显�???"
        self.select = 0  # select 用于选择采用的是哪种优化方式
        self.play_mode=1   # to determine the source of videos,If the play_mode is 1, then the video stream from the camera is being played
        self.name =name_list.copy()#pickle.load(open('./Characteristics/name1.pkl', mode='rb'))  # 读取姓名文件
        self.filename = None                #记录选择的文件夹�?
        self.videos_selected=None    # videos selected in the Map
        self.video_thread = None           #视频线程
        self.file_num=0                 #用于记录播放的当前文件夹的视频的序号
        self.frame_total=0              # the total number of frames of the video being played
        self.timer = QTimer(self)  # 3
        self.timer.start(50)
        self.semaphore=True    # used for
        self.person_detect_switch=False
        # self.detector = detector()
        # self.detector.init(gpu_id=0)
        # self.extractor = faceExtractor()
        # self.extractor.init(gpu_id=0, weight_file="/home/cliang/syx/demonstration/checkpoint.pth.tar",include_top=True)
        # self.deepsort = DeepSort(extractor=self.extractor)


    def init_connect(self):
        self.BTN_PLAY.clicked.connect(self.play)  # 播放
        self.BTN_PAUSE.clicked.connect(self.pause)  # 暂停
        self.BTN_RESTART.clicked.connect(self.restart)  # 重新播放
        # self.BTN_SHOW.clicked.connect(self.showTraits)  # 打印轨迹
        self.BTN_OPEN.clicked.connect(self.openFile)      #打开文件�?


        self.BTN_test.clicked.connect(self.change_state_of_detection)  # open the map
        self.Slider1.valueChanged.connect(self.change_pred_threshold)  # 修改pred_threshold，应用于func1
        self.Slider2.valueChanged.connect(self.change_judge_threshold)  # 修改judge_threshold，应用于func2
        # self.Slider_delay.valueChanged.connect(self.change_interval)
        self.comboBox_optimize.activated.connect(self.change_select)
        # self.label_map.pres.conncet(self.openMap)
        self.timer.timeout.connect(self.update_progressBar)
        self.progressBar.sliderPressed.connect(self.lockBar)
        self.progressBar.sliderReleased.connect(self.change_progressBar)
        self.progressBar.setMouseTracking(True)
        self.progressBar.installEventFilter(self.progressBar)  # 事件过滤�? to install eventfilter for the progressbar
        self.label_map.installEventFilter(self)  # 事件过滤器



    def init_GuiSettings(self):  # 用于设置GUI的一些属�?
        self.frame.setFrameShadow(QFrame.Sunken)  # 设置框架阴影
        pixmap = QPixmap("Distribution of cameras.jpg")  # 按指定路径找到图片
        self.label_map.setPixmap(pixmap)  # 在label_map上显示图片
        self.label_map.setScaledContents (True)  # 让图片自适应label大小

        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.label_map.setGraphicsEffect(effect)
        items=['0','1','2']
        self.comboBox_optimize.addItems(items)

    def init_mutex(self):

        self.mutex1=threading.Lock()     #the mutex1 lock used for
        self.mutex2=threading.Lock()     #the mutex2 lock used for self.count
        self.mutex3=threading.Lock()
        self.mutex4=threading.Lock()     # the mutex4 lock used for locking the progress bar
        self.mutex5 = threading.Lock()

    def func_selector(self, num, pt1, pt2, max_pred_index, max_pred):  # 优化方案选择�?
        if self.select == 0:  # 不选择任何优化方案
            flag = True
            self.no_func(num, pt1, pt2)
        elif self.select == 1:  # 选择优化方案1
            flag = self.func_1(num, max_pred, pt1, pt2)
        elif self.select == 2:  # 选择优化方案2
            max_pred, max_pred_index, flag = self.func_2(num, max_pred, max_pred_index, pt1, pt2)

        return max_pred, max_pred_index, flag

    def no_func(self, num, pt1, pt2):
        if str(num) in self.traits.keys():  # 检测这个目标之前是否已经在self.traits数组中保留过轨迹信息�?如果�?则在其轨迹信息之后接着记录
            self.traits[str(num)].append((pt1, pt2))
        else:
            self.traits[str(num)] = [(pt1, pt2)]  # 在字典中新增一个索�?并保留第一个轨迹信�?

    def func_1(self, num, max_pred, pt1, pt2):  # 优化方案1，当对于某一轨迹当前帧的max_pred大于参数threshold时，才将名字显示在视频中，否则显�???"
        if str(num) in self.traits.keys():  # 检测这个目标之前是否已经在self.traits数组中保留过轨迹信息�?如果�?则在其轨迹信息之后接着记录
            self.traits[str(num)].append((pt1, pt2))
        else:
            self.traits[str(num)] = [(pt1, pt2)]  # 在字典中新增一个索�?并保留第一个轨迹信�?

        if max_pred > self.pred_threshold:
            flag = True
        else:
            flag = False
        print(self.pred_threshold, max_pred, flag)
        return flag

    def func_2(self, num, max_pred, max_pred_index, pt1,
               pt2):  # 优化方案2: 统计最近limit次中是否最大的判断分数对应的索引是哪一个，并且，如果这个索引在最近limit次中出现的频率超过了judge_threshold,flag才为true
        if str(num) in self.traits.keys():  # 检测这个目标之前是否已经在self.traits数组中保留过轨迹信息�?如果�?则在其轨迹信息之后接着记录
            self.traits[str(num)].append((pt1, pt2))
        else:
            self.traits[str(num)] = [(pt1, pt2)]  # 在字典中新增一个索�?并保留第一个轨迹信�?

        if str(num) in self.historic_max_pre.keys():  # 检测这个目标之前是否已经在self.historic_max_pre数组中保留过轨迹信息�?如果�?则在其轨迹信息之后接着记录
            if (len(self.historic_max_pre[str(num)])) < self.update_limit:  # 判断这个轨迹记录的判定数组是否长度小�?0
                self.historic_max_pre[str(num)].append((max_pred_index, max_pred))

            else:
                del self.historic_max_pre[str(num)][0]
                self.historic_max_pre[str(num)].append((max_pred_index, max_pred))

        else:
            self.historic_max_pre[str(num)] = [(max_pred_index, max_pred)]  # 在historic_max_pre新增一个索�?保留当前的最大索引、最大索引分�?
        max_pred, max_pred_index, flag = self.count_and_find_max(self.historic_max_pre[str(num)])
        return max_pred, max_pred_index, flag

    def count_and_find_max(self, history):
        max = history[0][1]
        maxIndex = history[0][0]
        count = 0
        for i in range(0, len(history)):
            if (max < history[i][1]):
                max = history[i][1]
                maxIndex = history[i][0]

        for i in range(0, len(history)):
            if maxIndex == history[i][0]:
                count += 1

        frequency = count / (len(history))
        if frequency > self.judge_threshold:
            flag = True
        else:
            flag = False
        return max, maxIndex, flag

    def paint_chinese_opencv(self, img, chinese, pos, color, flag,isRevised=False):  # 在图像上显示中文
        # 图像从OpenCV格式转换成PIL格式
        if flag == False:
            chinese = "??"

        elif isRevised:
            color=(220,220,220)


        pos=(pos[0],pos[1]-20)  #使得名字出现在人脸上�?

        img_PIL = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        font = ImageFont.truetype('/usr/share/fonts/truetype/arphic/ukai.ttc', 20)
        draw = ImageDraw.Draw(img_PIL)
        draw.text(pos, chinese, font=font, fill=color)

        img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
        return img



    def playVideo1(self):                #在play函数中此函数被调�?

        self.playable = True
        jump_count=0        #跳帧计数，当计数值为2时会被重置为0
        jump_interval=1     #跳帧间隔�?�?
        count_nobody=50     #如果连续�?0次都没有检测到人，则开始快进模�?
        for video in self.videos_selected[self.file_num:]:
            self.videoCap = cv2.VideoCapture(video)
            self.frame_total = self.videoCap.get(7)  # get the total num of frames of the video being played
            self.progressBar.setMaximum(self.frame_total)
            print("Playing:" + video)
            print(self.frame_total)
            self.videoCap.set(cv2.CAP_PROP_POS_FRAMES, self.count)  # 设置从哪一帧开始播放视�?
            print("num:",self.videoCap.get(1))

            boxes=self.detect_boxes[video]

            while self.playable:  # 点击pause按钮时，playable会被设置成False
                time.sleep(0.05)
                self.mutex1.acquire()
                flag, frame = self.videoCap.read()
                self.mutex1.release()
                jump_count += 1
                jump_count = jump_count % jump_interval
                #
                # QApplication.processEvents()
                time.sleep(self.interval)
                if flag:
                    # The frame is ready and already captured
                    if jump_count == 0:
                        # frame, flag = self.draw_this_frame(frame, self.count)
                        if self.person_detect_switch:
                            frame=self.draw_boxes_for_detection(frame,self.count,boxes)
                        show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB
                        showImage = QImage(show.data, show.shape[1], show.shape[0],
                                           QImage.Format_RGB888)  # 转换成QImage类型
                        self.label.setScaledContents(True)
                        self.label.setPixmap(QPixmap.fromImage(showImage))  # 图像输出至label
                        # height, width, channel = frame.shape
                        # qImg = QImage(frame.data, width, height)
                        # self.label.setPixmap(QPixmap(qImg)

                    self.mutex2.acquire()
                    self.count += 1
                    self.mutex2.release()
                else:  # 如果当前视频播放完毕
                    # print("file: "+file+" 已经播放完毕,开始播放下一个视�?)
                    self.mutex2.acquire()
                    self.count = 0
                    self.mutex2.release()
                    self.file_num += 1  # 读取下一个视频，视频的名称都保存在files中，通过增加file_num的值来决定选择files数组中哪一个文件名
                    break
            if not self.playable:
                QApplication.processEvents()  # end while self.playable:
                print("GG!")
                break

        if self.playable:
          print("All the videos has finished")





    def playVideo2(self):                #在play函数中此函数被调�?
        self.playable = True
        jump_count=0        #跳帧计数，当计数值为2时会被重置为0
        jump_interval=2     #跳帧间隔�?�?
        count_nobody=50     #如果连续�?0次都没有检测到人，则开始快进模�?
        for root, dirs, files in os.walk(self.filename):
            while self.file_num<len(files):
                file=files[self.file_num]
                self.videoCap=cv2.VideoCapture(os.path.join(root, file))
                self.frame_total=self.videoCap.get(7)      # get the total num of frames of the video being played
                self.progressBar.setMaximum(self.frame_total)
                print("正在播放�?file:"+file)
                self.videoCap.set(cv2.CAP_PROP_POS_FRAMES, self.count)  # 设置从哪一帧开始播放视�?
                while self.playable:  # 点击pause按钮时，playable会被设置成False
                    time.sleep(0.02)
                    self.mutex1.acquire()
                    flag, frame = self.videoCap.read()
                    self.mutex1.release()
                    # self.progressBar.setValue(int(self.count/self.frame_total*100))
                    jump_count+=1
                    jump_count=jump_count%jump_interval

                    QApplication.processEvents()
                    time.sleep(self.interval)
                    # print(flag)
                    if flag:
                        # The frame is ready and already captured
                        if jump_count==0:
                            # frame,flag = self.draw_this_frame(frame, self.count)
                            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR转化成RGB
                            showImage = QImage(show.data, show.shape[1], show.shape[0],
                                               QImage.Format_RGB888)  # 转换成QImage类型
                            self.label.setScaledContents(True)
                            self.label.setPixmap(QPixmap.fromImage(showImage))  # 图像输出至label
                            # height, width, channel = frame.shape
                            # qImg = QImage(frame.data, width, height)
                            # self.label.setPixmap(QPixmap(qImg)

                        self.mutex2.acquire()
                        self.count += 1
                        self.mutex2.release()
                    else:                   #如果当前视频播放完毕
                        # print("file: "+file+" 已经播放完毕,开始播放下一个视�?)
                        self.mutex2.acquire()
                        self.count=0
                        self.mutex2.release()
                        self.file_num+=1       #读取下一个视频，视频的名称都保存在files中，通过增加file_num的值来决定选择files数组中哪一个文件名
                        break
                if not self.playable:
                    QApplication.processEvents()                   #end while self.playable:
                    break
        if self.playable:
          print("该文件夹下视频已全部播放完毕�?")
          QApplication.processEvents()



    def play(self):             #activated when button 'play' is clicked
        # """
        # :param choice: choice should be type of integer which denotes the pattern of playing. Default:1
        # :return:
        # """
        choice=self.play_mode
        if self.video_thread==None or self.video_thread.is_alive()==False:

            if choice ==1:            # choose the videos from cameras
                if self.videos_selected is None:
                    self.openMap(from_play=True)


                self.video_thread = threading.Thread(target=self.playVideo1)
                self.video_thread.start()
            elif choice == 2:  # choose a file which contains videos
                if self.filename == None:  # 如果尚未选择播放哪个文件夹的视频，就需要先选择文件�?相当于先点击了open按钮
                    self.openFile()
                self.video_thread = threading.Thread(target=self.playVideo2)
                self.video_thread.start()


    def pause(self):            #点击pause键的功能

        self.playable = False
        print(self.count)


    def restart(self):             #点击restart键的功能
        self.playable = False
        self.video_thread.join()        #让上一次play创建的子进程结束
        self.playable = True
        self.count =0  # 重置视频播放的当前帧�?
        self.file_num=0
        self.traits = {}  # 重置轨迹字典
        self.play()


    def showTraits(self):           #打印当前已经保存的轨�?
        print("\n\n")
        for i in self.traits.keys():
            print(i + "号轨迹：")
            print(self.traits[i])

    def change_pred_threshold(self, value):
        self.pred_threshold = value / 2.0
        self.label_threshold1.setText(str(self.pred_threshold))

    def change_judge_threshold(self, value):
        self.judge_threshold = value / 20.0  # 问：能不能这里除数变成slider的长�?
        self.label_threshold2.setText(str(self.judge_threshold))


    def change_select(self):
        self.select = self.comboBox_optimize.currentIndex()

    def change_interval(self, value):
        self.interval = value/1000
        self.label_delay.setText(str(self.interval) + 'ms')


    def update_progressBar(self):
        self.mutex4.acquire()
        if self.semaphore:
            self.mutex3.acquire()
            if self.frame_total!=0:
             self.progressBar.setValue(self.count)
            self.mutex3.release()
        self.mutex4.release()
        if self.frame_total!=0:
            self.progress_num.setText(str(round(float(self.count/self.frame_total*100),1))+"%")

    def openFile(self,filename=None):
        if self.video_thread != None and self.video_thread.is_alive() is not False:
            self.playable=False
            self.video_thread.join()
            self.playable=True
        self.play_mode=2    #change the play_mode
        if not filename :   # if filename is empty
           self.filename = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        else:
           self.filename=filename
        print(self.filename)
        print("您选择的文件夹下有以下文件�?")
        for root, dirs, files in os.walk(self.filename):
            for file in files:
                print(os.path.join(root, file));
        self.play()




    def openMap(self,from_play=False):
        self.play_mode=1
        Mymap = Map()
        Mymap.setAttribute(Qt.WA_DeleteOnClose)
        Mymap.Map_Signal.connect(self.get_Signal_from_Map)      #receive the signal from Map
        Mymap.exec_()


        if not from_play:
            self.video_thread = threading.Thread(target=self.playVideo1)
            self.video_thread.start()
        print(" end openMap")





    def lockBar(self):
        self.mutex4.acquire()
        self.semaphore=False
        self.mutex4.release()
    def prediction(self, img):
        detect = False
        im = Image.fromarray(img)
        img_size = np.asarray(img.shape)[0:2]
        bbox_xywh, landmarks = self.detector.detect(im, min_face_size=30.0)
        if len(bbox_xywh) > 0:
            cls_conf = [i[4] for i in bbox_xywh]
            bbox_xywh = [[(i[0]+i[2])/2, (i[1]+i[3])/2, i[2]-i[0], i[3]-i[1], i[4]] for i in bbox_xywh]
            outputs = self.deepsort.update(bbox_xywh, img)
            if len(outputs) > 0:
                bbox_xyxy = outputs[:, :4]
                identities = outputs[:, -1]
                imgs = []
                boxes = []
                for idx, bbox in enumerate(bbox_xyxy):
                    x1, y1, x2, y2 = convert_to_square(bbox,img_size,0.22)
                    imgs.append(img[y1:y2, x1:x2])
                    boxes.append([bbox[1], bbox[0], bbox[3], bbox[2]])
                pre = self.extractor.classifies(imgs)
                pre = pre.cpu().detach().numpy()
                detect = True
                return boxes, identities, pre
        if not detect:
            return [], None, None

    def change_progressBar(self):
        self.mutex3.acquire()
        self.mutex2.acquire()
        self.count=self.progressBar.value()
        self.historic_max_pre={}
        self.traits={}
        self.mutex2.release()

        self.mutex1.acquire()
        print(self.count)
        self.videoCap.set(cv2.CAP_PROP_POS_FRAMES, self.count)  # 设置从哪一帧开始播�?
        self.mutex1.release()
        self.mutex3.release()
        self.mutex4.acquire()
        self.semaphore=True
        self.mutex4.release()

    def draw_boxes_for_detection(self,frame,frame_id,boxes):
        if frame_id in boxes:
            boxes_for_this_frame=boxes[frame_id]
            for box in boxes_for_this_frame:
                pt1 = (box[0], box[1])  # 矩形左上角点
                pt2 = (box[2], box[3])  # 矩形右下角点
                cv2.rectangle(frame, pt1, pt2, (144,238,144), 3)
        else:
            pass
        return frame













    # def draw_this_frame(self, img, count):  # 为某一帧增加矩形框
    #
    #     boxes, identities, scores = self.prediction(img)
    #
    #
    #     for i in range(len(boxes)):
    #         pt1 = (boxes[i][1], boxes[i][0])  # 矩形左上角点
    #         pt2 = (boxes[i][3], boxes[i][2])  # 矩形右下角点
    #         num = identities[i]  # 轨迹的序�?\
    #         color=MyColor.colorsHub[num%MyColor.color_total]
    #         cv2.rectangle(img, pt1, pt2, color, 2)
    #         max_pred_index_old = np.argmax(scores[i])  # 得到对于该帧中某一轨迹的最大判断分数在name中的索引
    #         max_pred_old = scores[i][max_pred_index_old]  # 对于该帧中某一轨迹的最大判断分�?
    #         max_pred_new, max_pred_index_new, flag = self.func_selector(num, pt1, pt2, max_pred_index_old, max_pred_old)
    #         if max_pred_index_old == max_pred_index_new:
    #             img = self.paint_chinese_opencv(img, str(self.name[max_pred_index_new]), pt1, (0, 255, 0), flag,isRevised=False)
    #         else:
    #             img = self.paint_chinese_opencv(img, str(self.name[max_pred_index_new]), pt1, (0, 255, 0), flag,
    #                                             isRevised=True)
    #
    #     if scores is None:
    #         flag = False
    #     else:
    #         flag=True
    #     return img, flag

    def get_Signal_from_Map(self,connect):

        if self.video_thread != None and self.video_thread.is_alive()!=False:
            self.playable = False
            self.video_thread.join()        #让上一次play创建的子进程结束
            self.playable = True
        if connect is not None:
            print(connect)
            self.videos_selected=connect
            self.detect_boxes=self.get_boxes_of_detection(self.videos_selected)
            print(self.detect_boxes)
            self.count=0            # reset the count
            self.file_num = 0
            self.traits = {}  # 重置轨迹字典
        else:
            #maybe there could be a notification
            pass

    def get_boxes_of_detection(self,video_selected):
        boxes={}
        for video in video_selected:
            video_name = video.split('/')[-1]
            file_name = video.split('/')[-2]
            txt_name = video_name.replace("mp4","txt")
            txt_path=os.path.join(txt_root_path,file_name,txt_name)
            if not os.path.exists(txt_path):
                print("{} not exist",format(txt_path))
                boxes[video] = {}
            else:
                boxes[video] = {}
                with open(txt_path) as f:
                    for line in f.readlines():

                        line=line.split(' ')
                        frame_id=int(line[0])
                        x1=int(line[1])
                        y1=int(line[2])
                        x2 = int(line[3])
                        y2 = int(line[4])
                        if frame_id not in boxes[video]:
                          boxes[video][frame_id]=[[x1,y1,x2,y2]]
                        else:
                          boxes[video][frame_id].append([x1, y1, x2, y2])
                f.close()
        print(boxes)
        return boxes

    def change_state_of_detection(self):
        self.person_detect_switch=not self.person_detect_switch

            

    def eventFilter(self, object, event):


        if event.type() == QEvent.MouseButtonPress and object == self.label_map:
            self.openMap()
        elif event.type() == QEvent.Enter and object == self.label_map:
            Animation = AnimationShadowEffect(Qt.white, self.label_map)
            self.label_map.setGraphicsEffect(Animation)
            Animation.start()
        elif event.type() == QEvent.Leave and object == self.label_map:
            effect = QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(12)
            effect.setOffset(0, 0)
            effect.setColor(Qt.gray)
            self.label_map.setGraphicsEffect(effect)
        pass






if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_gui = myVideoProcessing()
    video_gui.setAttribute(Qt.WA_DeleteOnClose)
    video_gui.show()
    sys.exit(app.exec_())




