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

import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from guisupervisedlabeler import GuiSupervisedLabeler


class Ui_annotationWindow(object):

    def setupUi(self, annotationWindow, cocotaProject, screenDimensions, mainWindowForm):
        self.annotationWindow = annotationWindow
        self.project = cocotaProject
        self.mainWindowForm = mainWindowForm

        xScale, yScale = screenDimensions

        # self.getConfig()
        self.startAnootationBackend()

        self.windowHeight = 700*yScale
        self.windowWidth = 900*xScale

        self.gridLayoutWidgetWidth = int(220/900 * self.windowWidth)
        self.gridLayoutWidgetHeight = int(700/700 * self.windowHeight)


        annotationWindow.setObjectName("annotationWindow")
        annotationWindow.setEnabled(True)
        annotationWindow.resize(self.windowWidth, self.windowHeight)
        annotationWindow.setMinimumSize(QtCore.QSize(self.windowWidth, self.windowHeight))
        annotationWindow.setMaximumSize(QtCore.QSize(self.windowWidth, self.windowHeight))

        self.gridLayoutWidget = QtWidgets.QWidget(annotationWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(680*xScale, 0, self.gridLayoutWidgetWidth-1, self.gridLayoutWidgetHeight-1))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        self.gridLayout_buttons = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_buttons.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_buttons.setObjectName("gridLayout_buttons")
        
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setMaximumSize(QtCore.QSize(self.windowWidth, self.windowHeight))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        
        self.scrollAreaButtons = QtWidgets.QWidget()
        self.scrollAreaButtons.setGeometry(QtCore.QRect(1*xScale, 1*yScale, self.gridLayoutWidgetWidth-1, self.gridLayoutWidgetHeight+1))
        self.scrollAreaButtons.setObjectName("scrollAreaButtons")
        
        height = 5*yScale
        k = len(self.project.tags)

        # print("self.gridLayoutWidgetHeight/k", self.gridLayoutWidgetHeight/k)
        

        color_jump = int((255-150)/k)
        color_val = 150

        for i, tag in enumerate(sorted(self.project.tags.keys())):
            # print(height)

            new_button = QtWidgets.QPushButton(self.scrollAreaButtons)
            # new_button.setStyleSheet("background-color:rgb({},{},{})".format(color_val/1.5,color_val,color_val/1.5))
            color_val+=color_jump

            new_button.setGeometry(QtCore.QRect(0, height, self.gridLayoutWidgetWidth, self.gridLayoutWidgetHeight/k-2))
            height+=int(self.gridLayoutWidgetHeight/k)
            new_button.setText(tag)
            
            # button_font = new_button.font()
            # button_font.setPointSize(20);
            # new_button.setFont(button_font)

            new_button.clicked.connect(self.sendText)

        self.scrollArea.setWidget(self.scrollAreaButtons)
        self.gridLayout_buttons.addWidget(self.scrollArea, 0, 0, 1, 1)
        
        # Fonts
        font_general = QtGui.QFont()
        # font_general.setPointSize(10*yScale)
        # font_general.setPointSize(13*yScale)

        font_toolName = QtGui.QFont()
        # font_toolName.setPointSize(11*yScale)
        # font_toolName.setPointSize(13*yScale)
        font_toolName.setFamily("Simplified Arabic")

        font_fixed = QtGui.QFont()
        # font_fixed.setPointSize(8*yScale)
        # font_fixed.setPointSize(13*yScale)
        font_fixed.setFamily("Simplified Arabic")

        font_tokenName = QtGui.QFont()
        # font_tokenName.setPointSize(11*yScale)
        # font_tokenName.setPointSize(13*yScale)
        

        x_pos = (self.windowWidth - self.gridLayoutWidgetWidth)/2-191*xScale/2

        self.tag_toolName = QtWidgets.QLabel(annotationWindow)
        self.tag_toolName.setGeometry(QtCore.QRect(10*xScale, 665*yScale, 670*xScale, 20*yScale))
        self.tag_toolName.setFont(font_toolName)
        self.tag_toolName.setObjectName("tag_toolName")

        self.tag_labelingMode = QtWidgets.QLabel(annotationWindow)
        self.tag_labelingMode.setGeometry(QtCore.QRect(x_pos, 10*yScale, 370*xScale, 25*yScale))
        self.tag_labelingMode.setFont(font_general)
        self.tag_labelingMode.setObjectName("tag_labelingMode")
        self.tag_labelingMode_fixed = QtWidgets.QLabel(annotationWindow)
        self.tag_labelingMode_fixed.setGeometry(QtCore.QRect(10*xScale, 10*yScale, 100*xScale, 25*yScale))
        self.tag_labelingMode_fixed.setFont(font_fixed)
        self.tag_labelingMode_fixed.setObjectName("tag_labelingMode_fixed")       
        # self.tag_labelingMode_fixed.setStyleSheet("color:rgb(100,100,100)")

        self.tag_schedleInformation = QtWidgets.QLabel(annotationWindow)
        self.tag_schedleInformation.setGeometry(QtCore.QRect(x_pos, 100*yScale, 300*xScale, 25*yScale))
        self.tag_schedleInformation.setFont(font_general)
        self.tag_schedleInformation.setObjectName("tag_schedleInformation")
        self.tag_schedleInformation_fixed = QtWidgets.QLabel(annotationWindow)
        self.tag_schedleInformation_fixed.setGeometry(QtCore.QRect(10*xScale, 100*yScale, 120*xScale, 25*yScale))
        self.tag_schedleInformation_fixed.setFont(font_fixed)
        self.tag_schedleInformation_fixed.setObjectName("tag_schedleInformation")
        # self.tag_schedleInformation_fixed.setStyleSheet("color:rgb(100,100,100)")

        self.tag_activity = QtWidgets.QTextEdit(annotationWindow)
        self.tag_activity.setGeometry(QtCore.QRect(x_pos, 205*yScale, 370*xScale, 115*yScale))
        self.tag_activity.setObjectName("tag_activity")        

        self.tag_activity_fixed = QtWidgets.QLabel(annotationWindow)
        self.tag_activity_fixed.setGeometry(QtCore.QRect(10*xScale, 205*yScale, 125*xScale, 25*yScale))
        self.tag_activity_fixed.setFont(font_fixed)
        self.tag_activity_fixed.setObjectName("tag_activity_fixed")
        # self.tag_activity_fixed.setStyleSheet("color:rgb(100,100,100)")

        self.tag_activityIndex = QtWidgets.QLabel(annotationWindow)
        self.tag_activityIndex.setGeometry(QtCore.QRect(x_pos, 175*yScale, 200*xScale, 25*yScale))
        self.tag_activityIndex.setFont(font_general)
        self.tag_activityIndex.setObjectName("tag_activityIndex")
        self.tag_activityIndex_fixed = QtWidgets.QLabel(annotationWindow)
        self.tag_activityIndex_fixed.setGeometry(QtCore.QRect(10*xScale, 175*yScale, 200*xScale, 25*yScale))
        self.tag_activityIndex_fixed.setFont(font_fixed)
        self.tag_activityIndex_fixed.setObjectName("tag_activityIndex")
        # self.tag_activityIndex_fixed.setStyleSheet("color:rgb(100,100,100)")

        self.tag_token = QtWidgets.QLabel(annotationWindow)
        self.tag_token.setGeometry(QtCore.QRect(x_pos, 320*yScale, 300*xScale, 40*yScale))
        self.tag_token.setFont(font_tokenName)
        self.tag_token.setObjectName("tag_token")
        self.tag_token_fixed = QtWidgets.QLabel(annotationWindow)
        self.tag_token_fixed.setGeometry(QtCore.QRect(10*xScale, 320*yScale, 300*xScale, 40*yScale))
        self.tag_token_fixed.setFont(font_fixed)
        self.tag_token_fixed.setObjectName("tag_token_fixed")
        # self.tag_token_fixed.setStyleSheet("color:rgb(100,100,100)")
        
        self.tag_suggestion = QtWidgets.QLabel(annotationWindow)
        self.tag_suggestion.setGeometry(QtCore.QRect(x_pos, 350*yScale, 300*xScale, 40*yScale))
        self.tag_suggestion.setFont(font_tokenName)
        self.tag_suggestion.setObjectName("tag_suggestion")
        # self.tag_suggestion.setStyleSheet("color:rgb(255,100,100)")
        self.tag_suggestion_fixed = QtWidgets.QLabel(annotationWindow)
        self.tag_suggestion_fixed.setGeometry(QtCore.QRect(10*xScale, 350*yScale, 300*xScale, 40*yScale))
        self.tag_suggestion_fixed.setFont(font_fixed)
        self.tag_suggestion_fixed.setObjectName("tag_suggestion_fixed")        
        # self.tag_suggestion_fixed.setStyleSheet("color:rgb(100,100,100)")

        self.tag_availableTags = QtWidgets.QLabel(annotationWindow)
        self.tag_availableTags.setGeometry(QtCore.QRect(x_pos+210*xScale, 440*yScale, 200*xScale, 40*yScale))
        self.tag_availableTags.setFont(font_general)
        self.tag_availableTags.setObjectName("tag_availableTags")
        # self.tag_availableTags.setStyleSheet("color:rgb(100,200,100)")
        
        ###############
        ## Buttons

        self.button_acceptPrediction = QtWidgets.QPushButton(annotationWindow)
        # self.button_acceptPrediction.setStyleSheet("background-color:rgb(255,100,100)")
        self.button_acceptPrediction.setGeometry(QtCore.QRect(x_pos, 440*yScale, 191*xScale, 41*yScale))
        self.button_acceptPrediction.setObjectName("button_acceptPrediction")
        self.button_acceptPrediction.clicked.connect(self.sendText)

        self.button_skip = QtWidgets.QPushButton(annotationWindow)
        # self.button_skip.setStyleSheet("background-color:rgb(255,200,200)")
        self.button_skip.setGeometry(QtCore.QRect(x_pos, 490*yScale, 191*xScale, 23*yScale))
        self.button_skip.setObjectName("button_skip")
        self.button_skip.clicked.connect(self.labeler.skip)

        self.button_stats = QtWidgets.QPushButton(annotationWindow)
        # self.button_stats.setStyleSheet("background-color:rgb(255,255,125)")
        self.button_stats.setGeometry(QtCore.QRect(x_pos, 540*yScale, 191*xScale, 23*yScale))
        self.button_stats.setObjectName("button_stats")
        self.button_stats.clicked.connect(self.labeler.plot_stats)

        self.button_back = QtWidgets.QPushButton(annotationWindow)
        # self.button_back.setStyleSheet("background-color:rgb(220,220,220)")
        self.button_back.setObjectName("button_back")
        self.button_back.clicked.connect(self.labeler.go_back)
        self.button_back.setGeometry(QtCore.QRect(554*xScale, 490*yScale, 100*xScale, 23*yScale))


        self.button_addToReview = QtWidgets.QPushButton(annotationWindow)
        # self.button_addToReview.setStyleSheet("background-color:rgb(125,125,255)")
        self.button_addToReview.setObjectName("button_addToReview")
        self.button_addToReview.clicked.connect(self.labeler.addCurrentActivityToReviewList)
        self.button_addToReview.setGeometry(QtCore.QRect(10*xScale, 590*yScale, 651*xScale, 23*yScale))
        # self.button_addToReview.setGeometry(QtCore.QRect(10, 590*xScale, 651*yScale, 23*yScale))

        
        self.button_mainMenu = QtWidgets.QPushButton(annotationWindow)
        # self.button_mainMenu.setStyleSheet("background-color:rgb(200,200,200)")
        self.button_mainMenu.setGeometry(QtCore.QRect(554*xScale, 660*yScale, 100*xScale, 23*yScale))
        self.button_mainMenu.setObjectName("button_mainMenu")
        self.button_mainMenu.clicked.connect(self.goToMainWindow)
   
        self.retranslateUi(annotationWindow)
        QtCore.QMetaObject.connectSlotsByName(annotationWindow)

        
    def retranslateUi(self, annotationWindow):
        _translate = QtCore.QCoreApplication.translate
        annotationWindow.setWindowTitle(_translate("annotationWindow", "Annotation Window"))
        self.tag_labelingMode.setText(_translate("annotationWindow", "TextLabel"))
        self.tag_labelingMode_fixed.setText(_translate("annotationWindow", "Labeling Mode:"))
        
        self.tag_toolName.setText(_translate("annotationWindow", "CoCoTA"))
        self.tag_schedleInformation.setText(_translate("annotationWindow", "TextLabel"))
        self.tag_schedleInformation_fixed.setText(_translate("annotationWindow", "Current Document:"))

        self.tag_activity.setText(_translate("annotationWindow", "TextLabel"))
        self.tag_activity_fixed.setText(_translate("annotationWindow", "Current Sentence:"))
        self.tag_activityIndex.setText(_translate("annotationWindow", "TextLabel"))
        self.tag_activityIndex_fixed.setText(_translate("annotationWindow", "Current Sentence Index:"))

        self.tag_token.setText(_translate("annotationWindow", "TextLabel"))
        self.tag_token_fixed.setText(_translate("annotationWindow", "Current Token:"))
        self.tag_suggestion.setText(_translate("annotationWindow", "Available"))
        self.tag_suggestion_fixed.setText(_translate("annotationWindow", "Current Prediction:"))
        
        self.button_acceptPrediction.setText(_translate("annotationWindow", "Accept Prediction"))
        self.button_mainMenu.setText(_translate("annotationWindow", "Main Menu"))
        self.tag_availableTags.setText(_translate("annotationWindow", "or choose a label from the list: "))
        self.button_skip.setText(_translate("annotationWindow", "Skip Current Token"))
        self.button_addToReview.setText(_translate("annotationWindow", "Add Current Sentence to Review List"))
        # self.button_addPreviousToReview.setText(_translate("annotationWindow", "Add Previous Sentence to Review List"))
        # self.button_exit.setText(_translate("annotationWindow", "Exit"))
        self.button_stats.setText(_translate("annotationWindow", "Statistics"))
        self.button_back.setText(_translate("annotationWindow", "Back"))

    def startAnootationBackend(self):
        self.labeler = GuiSupervisedLabeler(self, self.project)

    def goToMainWindow(self):
        # self.annotationWindow.labeler.mode = "Regular"
        self.annotationWindow.close()
        self.mainWindowForm.show()

    def sendText(self):
        sender = self.annotationWindow.sender()
        buttonName = sender.text()
        self.labeler.getButtonText(buttonName)




# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     annotationWindow = QtWidgets.QWidget()
#     ui = Ui_annotationWindow()
#     ui.setupUi(annotationWindow)
#     annotationWindow.show()
    # sys.exit(app.exec_())

