# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Launcher.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Launcher(object):
    def setupUi(self, Launcher):
        Launcher.setObjectName("Launcher")
        Launcher.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(Launcher)
        self.gridLayout.setObjectName("gridLayout")
        self.lw_versions = QtWidgets.QListWidget(Launcher)
        self.lw_versions.setObjectName("lw_versions")
        self.gridLayout.addWidget(self.lw_versions, 0, 0, 1, 1)
        self.pb_startgame = QtWidgets.QPushButton(Launcher)
        self.pb_startgame.setEnabled(False)
        self.pb_startgame.setObjectName("pb_startgame")
        self.gridLayout.addWidget(self.pb_startgame, 1, 0, 1, 1)

        self.retranslateUi(Launcher)
        QtCore.QMetaObject.connectSlotsByName(Launcher)

    def retranslateUi(self, Launcher):
        _translate = QtCore.QCoreApplication.translate
        Launcher.setWindowTitle(_translate("Launcher", "Launcher"))
        self.pb_startgame.setText(_translate("Launcher", "开始游戏"))
