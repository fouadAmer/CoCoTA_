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

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append('./src/')
from mainWindow import ui_CoCoTAMainWindow
from initializationWindow import Ui_InitializationWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screenDimesions = app.desktop().screenGeometry()
    Form = QtWidgets.QWidget()
    ui = Ui_InitializationWindow()
    ui.setupUi(Form, screenDimesions)
    Form.show()
    sys.exit(app.exec_())
