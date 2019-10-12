'''
Author: Fouad Amer
Date: Augsut, 2019

Description:
This software, named CoCoTA (Consistent and Correct Text Anntations)
 is an active learning based text annotation tool. 
 More specifically, the software is target sequencial annotaiton tasks 
 such Part-of-Activity Tagging as described by Amer and Golparvard (2019).

This software is relased under an MIT license. 
If you are using this software for a scientific contribution, 
please include the following citation:

{
    Fouad Amer, Hui Yi Koh, and Mani Golparvar-Fard (2019), "
    Quick, Correct, and Consistent Text Annotations: An Active 
    Learning-Based Annotation Workflow and Tool for Sequence 
    Labeling of Construction Schedules". Construction Research 
    Congress 2020, March 8-10, Tempe, Arizona, US.
} 

'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QGraphicsObject
from PyQt5.QtCore import pyqtSignal

class ChooseNameWindow(QGraphicsObject):
    nameObtained = pyqtSignal(str, name='nameObtained')

    def setupUi(self, Form, initializationWindow):
        self.Form = Form
        Form.setObjectName("Form")
        x_scale, y_scale = initializationWindow.screenDimensions
        Form.resize(479*x_scale, 142*y_scale)
        self.textEdit = QtWidgets.QLineEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(30*x_scale, 50*y_scale, 430*x_scale, 31*y_scale))
        self.textEdit.setObjectName("textEdit")
        self.buttonSave = QtWidgets.QPushButton(Form)
        self.buttonSave.setGeometry(QtCore.QRect(240*x_scale, 100*y_scale, 100*x_scale, 25*y_scale))
        self.buttonSave.setObjectName("buttonSave")
        self.buttonCancel = QtWidgets.QPushButton(Form)
        self.buttonCancel.setGeometry(QtCore.QRect(360*x_scale, 100*y_scale, 100*x_scale, 25*y_scale))
        self.buttonCancel.setObjectName("buttonCancel")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30*x_scale, 20*y_scale, 430*x_scale, 16*y_scale))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.buttonSave.clicked.connect(self.savePressed)
        self.buttonCancel.clicked.connect(self.cancelPressed)

        self.nameObtained.connect(initializationWindow.getNewProjectName)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "New Project Name"))
        self.buttonSave.setText(_translate("Form", "Save"))
        self.buttonCancel.setText(_translate("Form", "Cancel"))
        self.label.setText(_translate("Form", "Please choose a name for your new annotation project:"))


    def savePressed(self):
        fileName = self.textEdit.text()
        if self.isOk(fileName):
            self.nameObtained.emit(fileName)
            self.Form.hide()
            return

    def isOk(self, fileName):
        msg = QMessageBox()
        if len(fileName.split())>1:
            msg.setText("the project name can not contain white spaces ..")
            msg.exec_()
            return False

        for char in fileName:
            if char in ['.',',','\'','\"','@','#','$','%','!', '^', '&', '*','(', ')', '?', '<', '>', ':', ';']:
                msg.setText("the project name can not contain punctuations nor symbols ..")
                msg.exec_()
                return False
        return True


    def cancelPressed(self):
        self.Form.close()
        return


