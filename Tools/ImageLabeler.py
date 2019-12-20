"""
By Fivethousand
"""


from GUI import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QFile, Qt, QEvent, QPoint, QTimer,QRect
from PyQt5.QtGui import QIcon, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QTreeWidgetItem,QLabel,QGridLayout,QPushButton
from functools import partial
import sys
import os


label_list=['0','1','2','3','4','5','6','7','8','9']            #修改标签的种类，直接在label_list中修改
MAX_COL=7   #there could be no more than MAX_COL images in a single row
IMG_SIZE=100


class ImagesLabeler(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ImagesLabeler, self).__init__()
        self.setupUi(self)
        self.init_gui()
        self.init_connect()
        self.init_data()



    def init_gui(self):

        self.display_area.setWidgetResizable(True)
        self.display_area.setObjectName("display_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 380, 280))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.display_area.setWidget(self.scrollAreaWidgetContents)
        self.grid = QGridLayout(self.scrollAreaWidgetContents)
        self.RDO_Single.setChecked(True)
        self.ComboxBox_Label.addItems(label_list)

    def init_connect(self):
        self.BTN_Open.clicked.connect(self.HandleOpen)
        self.BTN_Undo.clicked.connect(self.HandleRecentOpen)
        self.BTN_Undo1.clicked.connect(self.HandleUndo1)
        self.BTN_Undo2.clicked.connect(self.HandleUndo2)
        self.BTN_Confirm.clicked.connect(self.HandleConfirm)
        self.BTN_Pre.clicked.connect(self.HandlePre)
        self.BTN_Next.clicked.connect(self.HandleNext)
        self.BTN_Delete.clicked.connect(self.HandleDelete)
        self.BTN_Save.clicked.connect(self.HandleSave)
        self.RDO_Single.clicked.connect(self.read_txt)
        self.RDO_Pair.clicked.connect(self.read_txt)
        self.RDO_View.clicked.connect(self.HandleView)         #preview the list having been selected


    def init_data(self):
        self.filename = None  # the filename selected by user
        self.Item_name= None  # the name of the child node selected
        self.image1=None
        self.image2=None
        self.txt_list=[]
        self.list_pointer=-1    # to initialize this pointer as -1 which maps to the end of list
        self.recent_mode=None




    def HandleOpen(self):
        self.filename=QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        if self.filename:      #if  filename is not empty
            f=open('./RecentOpen.txt','a+')
            f.seek(0)
            f.truncate()  # 清空文件
            f.write(self.filename)
            f.close()
            self.read_txt()
            file_list = os.listdir(self.filename)
            file_list.sort()
            print(self.filename)
            print(file_list)
            # 设置根节点
            root = QTreeWidgetItem(self.treeWidget)
            root.setText(0,self.filename)
            for file in file_list:
                child1=QTreeWidgetItem(root)
                child1.setText(0,file)
                Image_list=os.listdir(os.path.join(self.filename, file))
                Image_list.sort()
                for image in Image_list:
                    child2 = QTreeWidgetItem(child1)
                    child2.setText(0,image)
            # 加载根节点的所有属性与子控件
            self.treeWidget.addTopLevelItem(root)
            self.treeWidget.clicked.connect(self.HandleFileClicked)
        else:
            print("The filename you selected is empty! Please re-open!")

    def HandleFileClicked(self,qmodeLindex):
        #delete all the widgets in the gridlayout
        for i in range(self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()
        item=self.treeWidget.currentItem()
        if item.childCount() is not 0 and item.parent() is not None:
            total=item.childCount()  #the total of the images in the file
            self.Item_name=item.text(0)
            Image_list=os.listdir(os.path.join(self.filename, item.text(0)))
            Image_list.sort()
            row=0
            col=0
            max_col=MAX_COL   #there could be no more than MAX_COL images in a single row

            for image in Image_list:
             label=QPushButton()
             label.setToolTip(image)
             label.setFixedSize(IMG_SIZE,IMG_SIZE)
             url=os.path.join(self.filename,item.text(0),image)
             url=self.filename+"/"+item.text(0)+"/"+image
             stylesheet="QPushButton{border-image: url("+url+")}"
             label.setStyleSheet(stylesheet)
             label.clicked.connect(partial(self.handleclicked,label.toolTip()))

             self.grid.addWidget(label,row,col)
             if (col+1)%max_col is 0:
                 col=0
                 row=row+1
             else:
                 col=col+1




    def handleclicked(self,name):
        if self.RDO_Single.isChecked() is True:
            if self.image1 is None:
                self.image1=self.filename+"/"+self.Item_name+"/"+name
                self.lbl_img1.setPixmap(QPixmap(self.image1))
                self.name1.setText(name)
                self.lbl_img1.setScaledContents(True)


        elif self.RDO_Pair.isChecked() is True:
            if self.image1 is None:
                self.image1 = self.filename + "/" + self.Item_name + "/" + name
                self.name1.setText(name)
                self.lbl_img1.setPixmap(QPixmap(self.image1))
                self.lbl_img1.setScaledContents(True)
            elif self.image2 is None:
                self.image2 = self.filename + "/" + self.Item_name + "/" + name
                self.name2.setText(name)
                self.lbl_img2.setPixmap(QPixmap(self.image2))
                self.lbl_img2.setScaledContents(True)

    def HandleRecentOpen(self):
       f=open('./RecentOpen.txt','r+')
       read_data = f.read()
       self.filename=read_data
       self.read_txt()
       file_list = os.listdir(self.filename)
       file_list.sort()

       # 设置根节点
       root = QTreeWidgetItem(self.treeWidget)
       root.setText(0, self.filename)
       for file in file_list:
           child1 = QTreeWidgetItem(root)
           child1.setText(0, file)
           Image_list = os.listdir(os.path.join(self.filename, file))
           Image_list.sort()
           for image in Image_list:
               child2 = QTreeWidgetItem(child1)
               child2.setText(0, image)

       # 加载根节点的所有属性与子控件
       self.treeWidget.addTopLevelItem(root)
       self.treeWidget.clicked.connect(self.HandleFileClicked)
    def HandleUndo1(self):
        self.image1=None    #clear the image having been selected
        self.lbl_img1.setPixmap(QPixmap(""))    #remove the img shown on the lbl_img1
        self.name1.setText("")

    def HandleUndo2(self):
        self.image2=None    #clear the image having been selected
        self.lbl_img2.setPixmap(QPixmap(""))    #remove the img shown on the lbl_img2
        self.name2.setText("")

    def HandleConfirm(self):
        if self.RDO_Single.isChecked() is True and self.image1 is not None:         #single mode
            self.txt_list.append(self.image1+' '+self.ComboxBox_Label.currentText())
            self.image1=None
            self.lbl_img1.setPixmap(QPixmap(""))  # remove the img shown on the lbl_img1
            self.name1.setText("")


        elif self.RDO_Pair.isChecked() is True and self.image1 is not None and self.image2 is not None :         #pair mode
            self.txt_list.append(self.image1+' '+self.image2+' '+self.ComboxBox_Label.currentText())
            self.image1 = None
            self.lbl_img1.setPixmap(QPixmap(""))  # remove the img shown on the lbl_img1
            self.name1.setText("")
            self.image2 = None  # clear the image having been selected
            self.lbl_img2.setPixmap(QPixmap(""))  # remove the img shown on the lbl_img2
            self.name2.setText("")

    def HandlePre(self):
        if self.RDO_View.isChecked() is True:       # View mode
            if self.txt_list:
                if len(self.txt_list)>=abs(self.list_pointer-1):        #to avoid an out_of_range index
                    self.list_pointer=self.list_pointer-1
                    if len(self.txt_list[0].split(
                            ' ')) == 2:  # in this way, we could judge whether the list is of single mode or not
                        # single mode
                        self.image1 = self.txt_list[self.list_pointer].split(' ')[0]
                        self.lbl_img1.setPixmap(QPixmap(self.image1))
                        self.lbl_img1.setScaledContents(True)
                    elif len(self.txt_list[0].split(' ')) == 3:
                        # pair mode
                        self.image1 = self.txt_list[self.list_pointer].split(' ')[0]
                        self.lbl_img1.setPixmap(QPixmap(self.image1))
                        self.lbl_img1.setScaledContents(True)
                        self.image2 = self.txt_list[self.list_pointer].split(' ')[1]
                        self.lbl_img2.setPixmap(QPixmap(self.image2))
                        self.lbl_img2.setScaledContents(True)
                else:           #the list_pointer has already mapped to the head of list
                    print("You are at the head of list !!!")

            else:
                print("the txtlist is empty!")
        else:               # not in view mode, then do nothing
            pass

    def HandleNext(self):
        if self.RDO_View.isChecked() is True:       # View mode
            if self.txt_list:
                if self.list_pointer+1<=-1:        #to avoid an out_of_range index
                    self.list_pointer=self.list_pointer+1
                    if len(self.txt_list[0].split(
                            ' ')) == 2:  # in this way, we could judge whether the list is of single mode or not
                        # single mode
                        self.image1 = self.txt_list[self.list_pointer].split(' ')[0]
                        self.lbl_img1.setPixmap(QPixmap(self.image1))
                        self.lbl_img1.setScaledContents(True)
                    elif len(self.txt_list[0].split(' ')) == 3:
                        # pair mode
                        self.image1 = self.txt_list[self.list_pointer].split(' ')[0]
                        self.lbl_img1.setPixmap(QPixmap(self.image1))
                        self.lbl_img1.setScaledContents(True)
                        self.image2 = self.txt_list[self.list_pointer].split(' ')[1]
                        self.lbl_img2.setPixmap(QPixmap(self.image2))
                        self.lbl_img2.setScaledContents(True)
                else:           #the list_pointer has already mapped to the head of list
                    print("You are at the botton of list !!!")

            else:
                print("the txtlist is empty!")
        else:               # not in view mode, then do nothing
            pass
    def HandleDelete(self):
        if self.txt_list:               # to avoid pop from empty list
            self.txt_list.pop(self.list_pointer)
            if self.txt_list:
                if abs(self.list_pointer) > len(self.txt_list):  # 当删去的图像位于list的头部，此时指针会发生越界，在此纠正这个错误
                    self.list_pointer += 1
                if len(self.txt_list[0].split(' '))==2:            # in this way, we could judge whether the list is of single mode or not
                    #single mode
                    self.image1 = self.txt_list[self.list_pointer].split(' ')[0]
                    self.lbl_img1.setPixmap(QPixmap(self.image1))
                    self.lbl_img1.setScaledContents(True)
                elif len(self.txt_list[0].split(' '))==3:
                    #pair mode
                    self.image1 = self.txt_list[self.list_pointer].split(' ')[0]
                    self.lbl_img1.setPixmap(QPixmap(self.image1))
                    self.lbl_img1.setScaledContents(True)
                    self.image2 = self.txt_list[self.list_pointer].split(' ')[1]
                    self.lbl_img2.setPixmap(QPixmap(self.image2))
                    self.lbl_img2.setScaledContents(True)
            else:
                self.image1 = ""
                self.lbl_img1.setPixmap(QPixmap(self.image1))
                self.image2 = ""
                self.lbl_img2.setPixmap(QPixmap(self.image2))
        else:
            print(" the list is empty！")



    def keyPressEvent(self, event):
        if str(event.key())=='16777220':        #响应回车，回车键按下时相当于确认
            self.HandleConfirm()


    def read_txt(self):
        self.txt_list=[]            #To begin with, Clear the list
        if self.RDO_Single.isChecked() is True:      # single mode
            self.recent_mode='Single'
            txtName="./txt_container/"+self.filename.split('/')[-1]+"_Single"+".txt"
            f= open(txtName, 'a+')
            for line in f.readlines():
                self.txt_list.append(line)

            f.close()
        elif self.RDO_Pair.isChecked() is True:        #pair mode
            self.recent_mode='Pair'
            txtName="./txt_container/"+self.filename.split('/')[-1]+"_Pair"+".txt"
            f = open(txtName, 'a+')
            for line in f.readlines():
                self.txt_list.append(line)
            f.close()

        print(self.txt_list)
    def HandleView(self):
        self.list_pointer=-1
        print(self.txt_list)
        if self.txt_list:
            if len(self.txt_list[0].split(' '))==2:            # in this way, we could judge whether the list is of single mode or not
                #single mode
                self.image1 = self.txt_list[self.list_pointer].split(' ')[0]
                self.lbl_img1.setPixmap(QPixmap(self.image1))
                self.lbl_img1.setScaledContents(True)
            elif len(self.txt_list[0].split(' '))==3:
                #pair mode
                self.image1 = self.txt_list[self.list_pointer].split(' ')[0]
                self.lbl_img1.setPixmap(QPixmap(self.image1))
                self.lbl_img1.setScaledContents(True)
                self.image2 = self.txt_list[self.list_pointer].split(' ')[1]
                self.lbl_img2.setPixmap(QPixmap(self.image2))
                self.lbl_img2.setScaledContents(True)

        else:
            print("the txtlist is empty!")

    def HandleSave(self):
        if self.recent_mode == 'Single':  # single mode
            txtName = "./txt_container/" + self.filename.split('/')[-1] + "_Single" + ".txt"
            f = open(txtName, 'a+')
        elif self.recent_mode == 'Pair':  # pair mode
            txtName = "./txt_container/" + self.filename.split('/')[-1] + "_Pair" + ".txt"
            f = open(txtName, 'a+')
        f.seek(0)
        f.truncate()  # 清空文件
        for i, line in enumerate(self.txt_list):
            if i != len(self.txt_list) - 1:
                f.write(line + "\n")
            else:
                f.write(line)
        f.close()


















if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = ImagesLabeler()
    myWin.setWindowFlags(Qt.Window)
    myWin.show()
    sys.exit(app.exec_())