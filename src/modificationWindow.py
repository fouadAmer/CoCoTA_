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
from PyQt5.QtWidgets import QMessageBox
from annotationWindow import Ui_annotationWindow


class Ui_modificationWindow(object):
    def setupUi(self, modificationWindow, project, screenDimensions, mainWindowForm):
        self.modificationWindow = modificationWindow
        self.mainWindowForm = mainWindowForm

        xScale, yScale = screenDimensions

        documents = list(project.input_labels_dict.keys())

        self.modificationWindow.setObjectName("modificationWindow")
        self.modificationWindow.resize(664*xScale, 648*yScale)
        self.tag_documentsAvailable = QtWidgets.QLabel(self.modificationWindow)
        self.tag_documentsAvailable.setGeometry(QtCore.QRect(20*xScale, 20*yScale, 201*xScale, 23*yScale))
        font = QtGui.QFont()
        # font.setPointSize(14*yScale)
        self.tag_documentsAvailable.setFont(font)
        self.tag_documentsAvailable.setObjectName("tag_documentsAvailable")
        self.tag_document = QtWidgets.QLabel(self.modificationWindow)
        self.tag_document.setGeometry(QtCore.QRect(20*xScale, 270*yScale, 391*xScale, 23*yScale))
        font = QtGui.QFont()
        # font.setPointSize(14*yScale)
        self.tag_document.setFont(font)
        self.tag_document.setObjectName("tag_document")
        self.text_documentIndex = QtWidgets.QPlainTextEdit(self.modificationWindow)
        self.text_documentIndex.setGeometry(QtCore.QRect(20*xScale, 310*yScale, 104*xScale, 30*yScale))
        self.text_documentIndex.setObjectName("text_documentIndex")
        self.tag_sentence = QtWidgets.QLabel(self.modificationWindow)
        self.tag_sentence.setGeometry(QtCore.QRect(20*xScale, 400*yScale, 391*xScale, 23*yScale))
        font = QtGui.QFont()
        # font.setPointSize(14*yScale)
        self.tag_sentence.setFont(font)
        self.tag_sentence.setObjectName("tag_sentence")
        self.text_sentenceIndex = QtWidgets.QPlainTextEdit(self.modificationWindow)
        self.text_sentenceIndex.setGeometry(QtCore.QRect(20*xScale, 440*yScale, 104*xScale, 30*yScale))
        self.text_sentenceIndex.setObjectName("text_sentenceIndex")
        self.text_tokenIndex = QtWidgets.QPlainTextEdit(self.modificationWindow)
        self.text_tokenIndex.setGeometry(QtCore.QRect(20*xScale, 560*yScale, 104*xScale, 30*yScale))
        self.text_tokenIndex.setObjectName("text_tokenIndex")
        self.tag_token = QtWidgets.QLabel(self.modificationWindow)
        self.tag_token.setGeometry(QtCore.QRect(20*xScale, 520*yScale, 391*xScale, 23*yScale))
        font = QtGui.QFont()
        # font.setPointSize(14*yScale)
        self.tag_token.setFont(font)
        self.tag_token.setObjectName("tag_token")
        self.button_submit = QtWidgets.QPushButton(self.modificationWindow)
        self.button_submit.setGeometry(QtCore.QRect(390*xScale, 600*yScale, 111*xScale, 25*yScale))
        self.button_submit.setObjectName("button_submit")
        self.button_cancel = QtWidgets.QPushButton(self.modificationWindow)
        self.button_cancel.setGeometry(QtCore.QRect(520*xScale, 600*yScale, 111*xScale, 25*yScale))
        self.button_cancel.setMinimumSize(QtCore.QSize(111*xScale, 0))
        self.button_cancel.setObjectName("button_cancel")
        self.list_availableDocuments = QtWidgets.QListWidget(self.modificationWindow)
        self.list_availableDocuments.setGeometry(QtCore.QRect(20*xScale, 60*yScale, 611*xScale, 192*yScale))
        self.list_availableDocuments.setObjectName("list_availableDocuments")

        for i, document in enumerate(project.input_labels_dict.keys()):
            self.list_availableDocuments.addItem('{}: {}'.format(i, document))
        
        self.retranslateUi(modificationWindow)
        QtCore.QMetaObject.connectSlotsByName(modificationWindow)

        self.button_cancel.clicked.connect(self.close)
        self.button_submit.clicked.connect(self.submit)
        
        self.annotationWindow = QtWidgets.QWidget()
        self.annotation_ui = Ui_annotationWindow()
        self.annotation_ui.setupUi(self.annotationWindow, project, screenDimensions, self.mainWindowForm)

    def retranslateUi(self, modificationWindow):
        _translate = QtCore.QCoreApplication.translate
        modificationWindow.setWindowTitle(_translate("modificationWindow", "Modification Window"))
        self.tag_documentsAvailable.setText(_translate("modificationWindow", "Available Documents"))
        self.tag_document.setText(_translate("modificationWindow", "Index of document to be modified:"))
        self.tag_sentence.setText(_translate("modificationWindow", "Index of sentence to be modified:"))
        self.tag_token.setText(_translate("modificationWindow", "Index of token to be modified:"))
        self.button_submit.setText(_translate("modificationWindow", "Submit"))
        self.button_cancel.setText(_translate("modificationWindow", "Back"))

    def close(self):
        self.modificationWindow.close()

    def submit(self):
        try:
            token_index = int(self.text_tokenIndex.toPlainText())
            sentence_index = int(self.text_sentenceIndex.toPlainText())
            document_index = int(self.text_documentIndex.toPlainText())
            # print(token_index, sentence_index, document_index)

        except:
            msg = QMessageBox()
            msg.setText("Make sure all the indexes are integers")
            msg.exec_()
            return
        
        self.annotationWindow.show()
        self.annotation_ui.labeler.modify(document_index, sentence_index, token_index)
        
