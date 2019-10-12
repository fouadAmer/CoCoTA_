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
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLineEdit

from cocota import Cocota
from chooseNameWindow import ChooseNameWindow
from mainWindow import ui_CoCoTAMainWindow
from comparer import Comparer


class Ui_InitializationWindow(object):
    def setupUi(self, Form, screenDimesions):
        self.Form = Form

        self.screenDimensions = (float(screenDimesions.height())/800,float(screenDimesions.width())/1280)
        xScale,yScale = self.screenDimensions

        Form.setObjectName("Form")
        Form.resize(410*xScale, 347*yScale)
        self.tag_toolName = QtWidgets.QLabel(Form)
        self.tag_toolName.setGeometry(QtCore.QRect(10*xScale, 320*yScale, 100*xScale, 20*yScale))
        font = QtGui.QFont()
        font.setFamily("Simplified Arabic")
        # font.setPointSize(15*yScale)
        self.tag_toolName.setFont(font)
        self.tag_toolName.setObjectName("tag_toolName")
        
        self.buttonNewProject = QtWidgets.QPushButton(Form)
        self.buttonNewProject.setGeometry(QtCore.QRect(80*xScale, 90*yScale, 251*xScale, 25*yScale))
        self.buttonNewProject.setObjectName("buttonNewProject")
        # self.buttonNewProject.setStyleSheet("background-color:rgb(200,250,200)")

        self.buttonExistingProject = QtWidgets.QPushButton(Form)
        self.buttonExistingProject.setGeometry(QtCore.QRect(80*xScale, 130*yScale, 251*xScale, 25*yScale))
        self.buttonExistingProject.setObjectName("buttonExistingProject")
        # self.buttonExistingProject.setStyleSheet("background-color:rgb(200,250,200)")

        self.buttonCompare = QtWidgets.QPushButton(Form)
        self.buttonCompare.setGeometry(QtCore.QRect(80*xScale, 210*yScale, 251*xScale, 24*yScale))
        self.buttonCompare.setObjectName("buttonCompare")
        # self.buttonCompare.setStyleSheet("background-color:rgb(250,150,150)")

        self.buttonExit = QtWidgets.QPushButton(Form)
        self.buttonExit.setGeometry(QtCore.QRect(330*xScale, 310*yScale, 71*xScale, 25*yScale))
        self.buttonExit.setObjectName("buttonExit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.buttonExit.clicked.connect(self.exitApplication)
        self.buttonNewProject.clicked.connect(self.startNewProject)
        self.buttonExistingProject.clicked.connect(self.openExistingProject)
        self.buttonCompare.clicked.connect(self.compareAnnotations)

        self.project = Cocota()


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "CoCoTA"))
        self.tag_toolName.setText(_translate("Form", "CoCoTA"))
        self.buttonNewProject.setText(_translate("Form", "Start New Project"))
        self.buttonExistingProject.setText(_translate("Form", "Open Existing Project"))
        self.buttonCompare.setText(_translate("Form", "Compare Annotations"))
        self.buttonExit.setText(_translate("Form", "Exit"))
        
    def exitApplication(self):
        exit()

    def startNewProject(self):
        input_directory = QFileDialog.getExistingDirectory(self.Form, 'Select directory')
        # print(input_directory)
        if input_directory != '':
            self.project.directory = input_directory
            NewNameForm = QtWidgets.QWidget()
            self.chooseName = ChooseNameWindow()
            self.chooseName.setupUi(NewNameForm, self)
            NewNameForm.show()

    def getNewProjectName(self, fileName):
        self.project.projectName = fileName
        # print("project directory: {}".format(self.project.directory))
        # print("project Name: {}".format(self.project.projectName))
        self.startmainWindow()
        self.Form.hide()


    def openExistingProject(self, fileName):
        fileName = QFileDialog.getOpenFileName(self.Form, 'Open file', 
            './',"cocota projects (*.cocota)")[0]

        # read data from the cocota file to populate the project
        self.project.projectName = fileName
        # print("project Name: {}".format(self.project.projectName))
        loadProjectSucceeded = self.project.load(fileName)
        if loadProjectSucceeded:
            self.startmainWindow()
            self.Form.hide()


    def startmainWindow(self):
        mainWindowForm = QtWidgets.QWidget()
        self.mainWindow = ui_CoCoTAMainWindow()
        self.mainWindow.setupUi(mainWindowForm, self.project, self.screenDimensions)
        mainWindowForm.show()


    def compareAnnotations(self):
        comparer = Comparer(self.Form)
        comparer.compareAnnotations()