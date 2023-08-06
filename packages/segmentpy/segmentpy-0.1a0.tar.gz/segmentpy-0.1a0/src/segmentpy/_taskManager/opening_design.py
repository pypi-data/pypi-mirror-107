# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/segmentpy/_taskManager/opening.ui',
# licensing of 'src/segmentpy/_taskManager/opening.ui' applies.
#
# Created: Fri May  7 22:46:04 2021
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(571, 355)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.log = QtWidgets.QLabel(Dialog)
        self.log.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.log.setObjectName("log")
        self.gridLayout.addWidget(self.log, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.log.setText(QtWidgets.QApplication.translate("Dialog", "Logging...", None, -1))

