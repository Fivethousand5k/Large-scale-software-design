"""
By Fivethousand
"""
from GUI_of_File_list import Ui_Form
from GUI_of_Map import Ui_MyMap
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal
from AnimationShadowEffect import AnimationShadowEffect  # @UnresolvedImport
import sys
import copy
import os

height=30
class File_list(Ui_Form,QDialog):
    List_Signal = pyqtSignal(list)

    def __init__(self,list,pos):
        """
        1.list contains the names of videos under the camera selected
        2.pos denotes the position of the radiobutton selected, which is used for determining that of File_list
        """
        self.list=list          # self.list will be converted into a variable type of Qcheckbox
        self.auxilary_list = copy.copy(self.list)       # So we prepare a copy for later use
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint) #how to make window stay on Top Hint?
        self.scrollBar = QWidget()
        self.scrollBar.setMinimumSize(250, len(list) * height + 30)
        self.scrollArea.setWidget(self.scrollBar)
        self.init_list()
        self.init_connect()


    def init_list(self):            #initialize the checkboxes in the scroll area
        number = 0
        for video_name in self.list:
            self.list[number] = QCheckBox(self.scrollBar)
            self.list[number].move(10, (number + 1) * height)
            # self.list[number].setChecked(True)
            self.list[number].setText(self.auxilary_list[number])
            number += 1

    def init_connect(self):
        self.Select_all.toggled.connect(self.handle_select_all)
        self.Btn_confirm.clicked.connect(self.handle_confirm)


    def handle_select_all(self):
        """
         #Attention!!!: at this time , self.list is type of QCheckbox as a consequence of the func init_list
        """
        if self.sender().isChecked():       #select all
            for btn in self.list:
                btn.setChecked(True)
        else:                               #select none
            for btn in self.list:
                btn.setChecked(False)

    def handle_confirm(self):
        videos_chosen=[]
        for btn in self.list:
            if btn.isChecked():
                videos_chosen.append(btn.text())

        self.List_Signal.emit(videos_chosen)   #launch the signals,and videos_chosen is a list containing the videos selected
        self.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyList=File_list(['a','b','c','ddd','a','b','c','ddd','a','b','c','ddd'],123)
    MyList.show()
    sys.exit(app.exec_())