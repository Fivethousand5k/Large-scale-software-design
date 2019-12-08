# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'offline.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GetROI(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.yellow, 2, Qt.SolidLine))
        painter.drawRect(rect)

        pqscreen = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))


class Ui_offline(object):
    def setupUi(self, offline):
        offline.setObjectName("offline")
        offline.resize(1216, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(offline.sizePolicy().hasHeightForWidth())
        offline.setSizePolicy(sizePolicy)
        offline.setMinimumSize(QtCore.QSize(1216, 720))
        offline.setMaximumSize(QtCore.QSize(9999, 9999))
        offline.setLayoutDirection(QtCore.Qt.LeftToRight)
        offline.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(offline)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_alg = QtWidgets.QWidget(offline)
        self.widget_alg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_alg.sizePolicy().hasHeightForWidth())
        self.widget_alg.setSizePolicy(sizePolicy)
        self.widget_alg.setMinimumSize(QtCore.QSize(1216, 30))
        self.widget_alg.setMaximumSize(QtCore.QSize(9999, 30))
        self.widget_alg.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_alg.setStyleSheet("background-color:#3C3C3C;color:white;\n"
"")
        self.widget_alg.setObjectName("widget_alg")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_alg)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_back2online = QtWidgets.QPushButton(self.widget_alg)
        self.btn_back2online.setObjectName("btn_back2online")
        self.horizontalLayout_2.addWidget(self.btn_back2online)
        spacerItem = QtWidgets.QSpacerItem(829, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget_alg)
        self.widge_title = QtWidgets.QWidget(offline)
        self.widge_title.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widge_title.sizePolicy().hasHeightForWidth())
        self.widge_title.setSizePolicy(sizePolicy)
        self.widge_title.setMinimumSize(QtCore.QSize(1200, 30))
        self.widge_title.setMaximumSize(QtCore.QSize(1200, 30))
        self.widge_title.setStyleSheet("")
        self.widge_title.setObjectName("widge_title")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widge_title)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_dir = QtWidgets.QLabel(self.widge_title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_dir.sizePolicy().hasHeightForWidth())
        self.label_dir.setSizePolicy(sizePolicy)
        self.label_dir.setMinimumSize(QtCore.QSize(70, 30))
        self.label_dir.setMaximumSize(QtCore.QSize(70, 30))
        self.label_dir.setStyleSheet("color:black;")
        self.label_dir.setObjectName("label_dir")
        self.horizontalLayout_3.addWidget(self.label_dir)
        self.text_dir = QtWidgets.QLineEdit(self.widge_title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_dir.sizePolicy().hasHeightForWidth())
        self.text_dir.setSizePolicy(sizePolicy)
        self.text_dir.setMinimumSize(QtCore.QSize(480, 30))
        self.text_dir.setMaximumSize(QtCore.QSize(480, 30))
        self.text_dir.setStyleSheet("background-color:white;color:black;")
        self.text_dir.setObjectName("text_dir")
        self.horizontalLayout_3.addWidget(self.text_dir)
        self.btn_open = QtWidgets.QPushButton(self.widge_title)
        self.btn_play = QtWidgets.QPushButton(self.widge_title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_open.sizePolicy().hasHeightForWidth())
        self.btn_open.setSizePolicy(sizePolicy)
        self.btn_open.setStyleSheet("background-color:#EAEAEA;color:black;")
        self.btn_open.setObjectName("btn_open")
        self.horizontalLayout_3.addWidget(self.btn_open)
        self.btn_play.setSizePolicy(sizePolicy)
        self.btn_play.setStyleSheet("background-color:#EAEAEA;color:black;")
        self.btn_play.setObjectName("btn_play")
        self.horizontalLayout_3.addWidget(self.btn_play)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.widge_title)
        self.widget_main = QtWidgets.QWidget(offline)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_main.sizePolicy().hasHeightForWidth())
        self.widget_main.setSizePolicy(sizePolicy)
        self.widget_main.setMinimumSize(QtCore.QSize(1200, 580))
        self.widget_main.setMaximumSize(QtCore.QSize(1200, 580))
        self.widget_main.setStyleSheet("")
        self.widget_main.setObjectName("widget_main")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_main)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.play_show = GetROI(self.widget_main)
        self.play_show2 = GetROI(self.widget_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.play_show.sizePolicy().hasHeightForWidth())
        self.play_show.setSizePolicy(sizePolicy)
        self.play_show.setMinimumSize(QtCore.QSize(850, 480))
        self.play_show.setMaximumSize(QtCore.QSize(850, 480))
        self.play_show.setText("")
        self.play_show.setObjectName("play_show")
        self.horizontalLayout.addWidget(self.play_show)

        self.play_show2.setSizePolicy(sizePolicy)
        self.play_show2.setMinimumSize(QtCore.QSize(850, 480))
        self.play_show2.setMaximumSize(QtCore.QSize(850, 480))
        self.play_show2.setText("")
        self.play_show2.setObjectName("play_show2")
        self.play_show2.hide()
        self.horizontalLayout.addWidget(self.play_show2)

        self.verticalLayout.addWidget(self.widget_main)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(offline)
        QtCore.QMetaObject.connectSlotsByName(offline)

    def retranslateUi(self, offline):
        _translate = QtCore.QCoreApplication.translate
        offline.setWindowTitle(_translate("offline", "Dialog"))
        self.btn_back2online.setText(_translate("offline", "返回在线处理"))
        self.label_dir.setText(_translate("offline", "当前路径"))
        self.btn_open.setText(_translate("offline", "打开"))
        self.btn_play.setText(_translate("offline", "暂停"))

