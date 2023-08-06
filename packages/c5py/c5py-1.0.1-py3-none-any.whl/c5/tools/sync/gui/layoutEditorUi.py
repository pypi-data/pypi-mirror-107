# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layoutEditor.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LayoutDialog(object):
    def setupUi(self, LayoutDialog):
        LayoutDialog.setObjectName("LayoutDialog")
        LayoutDialog.resize(401, 266)
        self.verticalLayout = QtWidgets.QVBoxLayout(LayoutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.preview = LayoutPreview(LayoutDialog)
        self.preview.setObjectName("preview")
        self.verticalLayout.addWidget(self.preview)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(LayoutDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(LayoutDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LayoutDialog)
        QtCore.QMetaObject.connectSlotsByName(LayoutDialog)

    def retranslateUi(self, LayoutDialog):
        _translate = QtCore.QCoreApplication.translate
        LayoutDialog.setWindowTitle(_translate("LayoutDialog", "Dialog"))
        self.pushButton.setText(_translate("LayoutDialog", "PushButton"))

from layout_preview import LayoutPreview
