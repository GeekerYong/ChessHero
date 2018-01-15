# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qtmain.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from pyhooked import Hook, KeyboardEvent
import win32gui
import time
import sys
from PyQt5.QtCore import *
import util.search as sch
import util.ocr as ocr
import os


def main(self):
    # 开始计时
    start = time.time()
    printStr = ""
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png screenshot.png")
    question, answer = ocr.ocr_result('./screenshot.png')
    print('问题:%s' % question)
    printStr = printStr + '问题:' + question +'\n'
    score, results, counts = sch.get_search_result(question, answer)
    for i in range(len(results)):
        count = 0
        print("#####################[%s](搜索结果数目:%s)(页面词频:%s)#########################" % (answer[i], score[i], counts[i]))
        printStr = printStr + "#####################[%s](搜索结果数目:%s)(页面词频:%s)#########################" % (answer[i], score[i], counts[i]) +'\n'
        for abst in results[i]:
            print(abst.abstract)
            printStr = printStr+ abst.abstract +'\n'
            count = count + 1
            if (count == 2):
                break
    end = time.time()
    self.textBrowser.setPlainText(printStr)
    print('程序用时：' + str(end - start) + '秒')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 462)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 150, 850, 271))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 40, 111, 91))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 0, 311, 171))
        self.label.setObjectName("label")
        self.pushButton.clicked.connect(self.check_main)
        # MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 584, 23))
        # self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def check_main(self):
        hld = win32gui.FindWindow(None, vm_name)
        if hld > 0:
            print('辅助运行中...\n题目出现的时候按F2，开启自动搜索\n')
            self.textBrowser.setPlainText('辅助运行中...\n题目出现的时候按F2，开启自动搜索\n')
        else:
            self.textBrowser.setPlainText('启动失败！\n模拟器（' + vm_name + '）未启动!')
            print('模拟器（' + vm_name + '）未启动!')

    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_F2):
            main(self)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "超级瞄准 V1.0.0"))
        self.pushButton.setText(_translate("MainWindow", "启用辅助"))
        self.label.setText(_translate("MainWindow", "本工具使用方法：\n"
"1，配置安卓模拟器，分辨率参数720x1280,dpi240。\n"
"2，进入对应答题应用的答题界面。\n"
"3，点击右边按钮运行本工具。\n"
"4，题目出现时按下F2键，程序将在2~3秒返回结果。\n"
"\n"
"本程序答案不能保证100%全对，但具有重要的参考价值。"))


class superWindow(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        super(superWindow, self).__init__()
        self.setupUi(self)

vm_name = "BlueStacks App Player"

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    superApp = superWindow()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("./Minicon.ico"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
    superApp.setWindowIcon(icon)
    superApp.show()
    sys.exit(app.exec_())
