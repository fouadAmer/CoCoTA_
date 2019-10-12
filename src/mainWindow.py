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

from annotationWindow import Ui_annotationWindow
from modificationWindow import Ui_modificationWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import os
import json

class ui_CoCoTAMainWindow(object):
    def setupUi(self, Form, cocotaProject, screenDimensions):
        self.Form = Form
        self.project = cocotaProject

        self.screenDimensions = screenDimensions
        xScale,yScale = self.screenDimensions

        Form.setObjectName("Form")
        Form.resize(410*xScale, 377*yScale)

        self.buttonLabels = QtWidgets.QPushButton(Form)
        self.buttonLabels.setGeometry(QtCore.QRect(60*xScale, 40*yScale, 300*xScale, 25*yScale))
        self.buttonLabels.setObjectName("buttonNew")
        # self.buttonLabels.setStyleSheet("background-color:rgb(200,200,250)")

        self.buttonNew = QtWidgets.QPushButton(Form)
        self.buttonNew.setGeometry(QtCore.QRect(60*xScale, 70*yScale, 300*xScale, 25*yScale))
        self.buttonNew.setObjectName("buttonNew")
        # self.buttonNew.setStyleSheet("background-color:rgb(200,200,250)")

        self.buttonRegulary = QtWidgets.QPushButton(Form)
        self.buttonRegulary.setGeometry(QtCore.QRect(60*xScale, 120*yScale, 300*xScale, 25*yScale))
        self.buttonRegulary.setObjectName("buttonRegulary")
        # self.buttonRegulary.setStyleSheet("background-color:rgb(200,250,200)")
        self.buttonSkipped = QtWidgets.QPushButton(Form)
        self.buttonSkipped.setGeometry(QtCore.QRect(60*xScale, 150*yScale, 300*xScale, 25*yScale))
        self.buttonSkipped.setObjectName("buttonSkipped")
        # self.buttonSkipped.setStyleSheet("background-color:rgb(200,250,200)")
        self.buttonRevision = QtWidgets.QPushButton(Form)
        self.buttonRevision.setGeometry(QtCore.QRect(60*xScale, 180*yScale, 300*xScale, 25*yScale))
        self.buttonRevision.setObjectName("buttonRevision")
        # self.buttonRevision.setStyleSheet("background-color:rgb(200,250,200)")
        self.buttonModifyPrevious = QtWidgets.QPushButton(Form)
        self.buttonModifyPrevious.setGeometry(QtCore.QRect(60*xScale, 210*yScale, 300*xScale, 25*yScale))
        self.buttonModifyPrevious.setObjectName("buttonModifyPrevious")
        # self.buttonModifyPrevious.setStyleSheet("background-color:rgb(200,250,200)")

        self.loadAssistant = QtWidgets.QPushButton(Form)
        self.loadAssistant.setGeometry(QtCore.QRect(60*xScale, 270*yScale, 300*xScale, 25*yScale))
        self.loadAssistant.setObjectName("loadAssistant")
        # self.buttonExportAnnotations.setStyleSheet("background-color:rgb(250,150,150)")

        self.buttonExportAnnotations = QtWidgets.QPushButton(Form)
        self.buttonExportAnnotations.setGeometry(QtCore.QRect(60*xScale, 300*yScale, 300*xScale, 25*yScale))
        self.buttonExportAnnotations.setObjectName("buttonExportAnnotations")
        # self.buttonExportAnnotations.setStyleSheet("background-color:rgb(250,150,150)")

        self.buttonExit = QtWidgets.QPushButton(Form)
        self.buttonExit.setGeometry(QtCore.QRect(330*xScale, 340*yScale, 71*xScale, 31*yScale))
        self.buttonExit.setObjectName("ButtonExit")
        self.tag_toolName = QtWidgets.QLabel(Form)
        self.tag_toolName.setGeometry(QtCore.QRect(10*xScale, 350*yScale, 100*xScale, 20*yScale))
        font = QtGui.QFont()
        font.setFamily("Simplified Arabic")
        # font.setPointSize(15*yScale)
        self.tag_toolName.setFont(font)
        self.tag_toolName.setObjectName("tag_toolName")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.buttonLabels.clicked.connect(self.addNewLabels)
        self.buttonExit.clicked.connect(self.exitApplication)
        self.buttonNew.clicked.connect(self.addNewSchedule)
        self.buttonExportAnnotations.clicked.connect(self.exportAnnotations)


        if len(self.project.input_sequences_dict) == 0 or len(self.project.tags)==0:
            self.buttonNew.setEnabled(False)
            self.buttonRegulary.setEnabled(False)
            self.buttonRevision.setEnabled(False)
            self.buttonSkipped.setEnabled(False)
            self.buttonModifyPrevious.setEnabled(False)
            self.loadAssistant.setEnabled(False)
            self.buttonExportAnnotations.setEnabled(False)

        else:
            self.setupAnnotationWindow()


    def setupAnnotationWindow(self):
        self.buttonRegulary.clicked.connect(self.runRegularAnnotationWindow)
        self.buttonSkipped.clicked.connect(self.runSkippedAnnotationWindow)
        self.buttonRevision.clicked.connect(self.runReviseAnnotationWindow)
        self.buttonModifyPrevious.clicked.connect(self.runModifyAnnotationWindow)
        self.loadAssistant.clicked.connect(self.runLoadAssistant)

        self.annotationWindow = QtWidgets.QWidget()
        self.annotation_ui = Ui_annotationWindow()
        self.annotation_ui.setupUi(self.annotationWindow, self.project, self.screenDimensions, self.Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Project Management Window"))
        self.buttonNew.setText(_translate("Form", "Load a New Document"))
        self.buttonLabels.setText(_translate("Form", "Set Up New Tags"))

        self.buttonRegulary.setText(_translate("Form", "Start or Continue Labeling Regularly"))
        self.buttonSkipped.setText(_translate("Form", "Label Previously Skipped Activities"))
        self.buttonRevision.setText(_translate("Form", "Label Activities in Revision List"))
        self.buttonModifyPrevious.setText(_translate("Form", "Modify Previous Labels"))
        self.buttonExportAnnotations.setText(_translate("Form", "Export Annotations"))
        self.loadAssistant.setText(_translate("Form", "Load Trained Assistant"))

        self.buttonExit.setText(_translate("Form", "Exit"))
        self.tag_toolName.setText(_translate("Form", "CoCoTA"))


    def exitApplication(self):
        exit()

    def addNewSchedule(self):
        fname = QFileDialog.getOpenFileName(self.Form, 'Open file', 
            './',"Text files (*.txt)")[0]

        if fname != '':
            # print(fname)
            data, entryName = self.read(fname)
            
            if entryName in self.project.input_sequences_dict:
                rev = 1
                extenstion = entryName.split('.')[-1]
                entryName = entryName.split('.')[0]
                newEntryName='{}_Rev0{}.{}'.format(entryName, rev, extenstion)

                while newEntryName in self.project.input_sequences_dict:
                    rev+=1
                    newEntryName='{}_Rev0{}.{}'.format(entryName, rev, extenstion)

                entryName = newEntryName
                
            self.project.input_sequences_dict[entryName] = data
            self.project.save()

            msg = QMessageBox()
            msg.setText("the new file has been added to {} data..".format(self.project.projectName))
            msg.exec_()

            self.buttonRegulary.setEnabled(True)
            self.buttonRevision.setEnabled(True)
            self.buttonSkipped.setEnabled(True)
            self.buttonModifyPrevious.setEnabled(True)
            self.loadAssistant.setEnabled(True)
            self.buttonExportAnnotations.setEnabled(True)
            self.setupAnnotationWindow()       


    def addNewLabels(self):
        fname = QFileDialog.getOpenFileName(self.Form, 'Open file', 
            './',"Text files (*.txt)")[0]

        if fname != '':
            # print(fname)
            data = self.read_tags(fname)
            self.project.tags = data

            msg = QMessageBox()
            msg.setText("the new tags have been successfully added..")
            msg.exec_()

            self.buttonNew.setEnabled(True)

    def read(self, fileName):
        file = open(fileName, 'r', encoding='utf-8')
        newFileName = fileName.split('/')[-1]
        # print(newFileName)
        data = {}
        counter = 0
        for line in file.readlines():
            # sentences = line.split('.')
            # for sentence in sentences:
            #     if len(sentence)>0:
            #         tokens = sentence.split()
            #         if len(tokens) > 0:
            #             data[str(counter)] = tokens
            #             print(tokens)
            #             counter+=1

            if len(line)>0:
                tokens_ = line.split()
                tokens = [token.strip(";:,./'[]()*&^%$#@!~<>") for token in tokens_]
                if len(tokens) > 0:
                    data[str(counter)] = tokens
                    # print(tokens)
                    counter+=1
        return data, newFileName

    def read_tags(self, fileName):
        file = open(fileName, 'r')
        tags = {}
        counter = 0
        for tag in file.readlines():
            tags[tag.rstrip()] = counter
            counter+=1
        return tags

    def exportAnnotations(self, local=True):
        exportDict = {}
        exportDict['labels'] = self.project.input_labels_dict
        exportDict['sentences'] = self.project.input_sequences_dict

        # if local:
        # print(local)
        # with open("current_project_annotations.json",'w') as outfile:
        #     json.dump(exportDict, outfile)
        # else:
        with open("{}/{}_annotations.json".format(self.project.directory, self.project.projectName),'w') as outfile:
            json.dump(exportDict, outfile)



        msg = QMessageBox()
        msg.setText("Annotations are successfully exported as a JSON file.\n\'labels\' contains the created labels.\n\'sentences\' contains all the input sequences.")
        msg.exec_()

    def runLoadAssistant(self):
        fname = QFileDialog.getOpenFileName(self.Form, 'Open file', 
            './',"CoCoTA Assistant files (*.acocota)")[0]

        msg = QMessageBox()
        try:
            with open(fname, 'r') as inFile:
                loaded_assistant = json.load(inFile)

            for key in loaded_assistant["unigrams"]:
                for key2, value in loaded_assistant["unigrams"][key].items():
                    self.project.probabilisticAssistant.unigrams[key][key2] = int(value)

            for key in loaded_assistant["bigrams"]:
                for key2, value in loaded_assistant["bigrams"][key].items():
                    self.project.probabilisticAssistant.bigrams[key][key2] = int(value)

            for key in loaded_assistant["trigrams"]:
                for key2, value in loaded_assistant["trigrams"][key].items():
                    self.project.probabilisticAssistant.trigrams[key][key2] = int(value)

            for key in loaded_assistant["bigramSurroundings"]:
                for key2, value in loaded_assistant["bigramSurroundings"][key].items():
                    self.project.probabilisticAssistant.bigramSurroundings[key][key2] = int(value)

            for key in loaded_assistant["trigramSurroundings"]:
                for key2, value in loaded_assistant["trigramSurroundings"][key].items():
                    self.project.probabilisticAssistant.trigramSurroundings[key][key2] = int(value)

            msg.setText("the trained Assistant has been successfully loaded..")
        except:
            msg.setText("the chosen assistant file is not valid!")
            
        msg.exec_()
        return

    def runRegularAnnotationWindow(self):
        self.annotationWindow.show()
        self.annotation_ui.labeler.labelNewSet()
        self.Form.hide()

    def runSkippedAnnotationWindow(self):
        # add a gui to pic the schedule and enter the index
        skippedExist = self.annotation_ui.labeler.labelSkipped()
        if skippedExist:
            self.annotationWindow.show()
            self.Form.hide()

    def runReviseAnnotationWindow(self):
        reviewExist = self.annotation_ui.labeler.review()
        if reviewExist:
            self.annotationWindow.show()
            self.Form.hide()

    def runModifyAnnotationWindow(self):
        self.modificationWindow = QtWidgets.QWidget()
        self.modification_ui = Ui_modificationWindow()
        self.modification_ui.setupUi(self.modificationWindow, self.project, self.screenDimensions, self.Form)
        self.modificationWindow.show()
        self.Form.hide()


