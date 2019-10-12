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
from collections import defaultdict

from cocota import Cocota

class Comparer():
    def __init__(self, Form):
        self.Form = Form

    def compareAnnotations(self):
        msg = QMessageBox()
        msg.setText("Please choose two projects (one at a time) to be compared")
        msg.exec_()

        uploadSuccessfull = True
        project_1 = Cocota()
        firstProject = QFileDialog.getOpenFileName(self.Form, 'Open file', 
            './',"cocota projects (*.cocota)")[0]
        loadProject_1_Successfull = project_1.load(firstProject)
        
        if loadProject_1_Successfull:
            # print("first project successfully loaded - {}".format(project_1.directory))
            project_2 = Cocota()
            secondProject = QFileDialog.getOpenFileName(self.Form, 'Open file', 
                './',"cocota projects (*.cocota)")[0]
            loadProject_2_Successfull = project_2.load(secondProject)
            
            if not loadProject_2_Successfull:
                uploadSuccessfull = False
            # else:
            #     print("second project successfully loaded".format(project_2.directory))
        else:
            uploadSuccessfull = False

        
        if uploadSuccessfull:
            results = {}
            Annotator_1 = 'A1'+project_1.projectName
            Annotator_2 = 'A2'+project_2.projectName
            results[Annotator_1] = defaultdict(int)
            results[Annotator_2] = defaultdict(int)

            accuracy = 0
            total = 0

            report = ''
            report, results, accuracy, total, seenSent, seenLab = self.getDiffernece(project_1, project_2, report, [], [], 
                                                                        results, accuracy, total, Annotator_1, Annotator_2)
            report+='\n\n'
            report, results, accuracy, total, seenSent, seenLab = self.getDiffernece(project_2, project_1, report, seenSent, seenLab, 
                                                                        results, accuracy, total, Annotator_2, Annotator_1)
            
            kappa, p0, pe = self.getKappa(results, accuracy, total)

            report+='\n\n'
            report+='Kappa: {}\nP0: {}\nPe: {}\n'.format(kappa, p0, pe)
            report+='\n\n...End of Report...'

            # print(report)

            output1 = open(project_1.directory+'/Report_{}_{}.txt'.format(project_1.projectName, project_2.projectName), 'w', encoding="utf-8")
            output1.write(report)
            output1.close()

            output2 = open(project_2.directory+'/Report_{}_{}.txt'.format(project_1.projectName, project_2.projectName), 'w', encoding="utf-8")
            output2.write(report)
            output2.close()

            msg = QMessageBox()
            msg.setText("Comparison was conducted successfully.\nIAA Kappa was found to be {}.\nDetailed copies of the report can be found in both project directories.".format(round(kappa,4)))
            msg.exec_()

    def getDiffernece(self, p1, p2, report, seenSentences, seenLabels, results, accuracy, total, Annotator_1, Annotator_2):
        for document in p1.input_labels_dict:

            if document in p2.input_labels_dict:
                document_has_differences = False
                document_added = False

                for sent_index in p1.input_labels_dict[document]:
                    sentence_added_to_report = False
                    if (document, sent_index) not in seenSentences:
                        seenSentences.append((document, sent_index))

                        sentence = p1.input_sequences_dict[document][sent_index]
                        
                        report_sentence = ''
                        
                        for i, label1 in enumerate(p1.input_labels_dict[document][sent_index]):
                            if sent_index in p2.input_labels_dict[document]:
                                if (document, sent_index, i) not in seenLabels:
                                    label2 = p2.input_labels_dict[document][sent_index][i]
                                    seenLabels.append((document, sent_index, i))

                                    results[Annotator_1][label1]+=1
                                    results[Annotator_2][label2]+=1
                                    total+=1

                                    if label1 != label2:
                                        if not sentence_added_to_report:
                                            report_sentence+='\nDifferences in Sentence: {}\n'.format(sent_index)
                                            sentence_added_to_report = True

                                        report_sentence+='label {} ({}): \"{}\" in {} but \"{}\" in {}\n'.format(i, sentence[i],label1, p1.projectName, label2, p2.projectName)
                                        document_has_differences=True
                                    else:
                                        accuracy+=1

                            else:
                                report_sentence+='Sentence {} is in {} but not in {}\n'.format(sent_index, p1.projectName, p2.projectName)
                                

                    if document_has_differences:
                        if not document_added:
                            report+='\nDifferences in docuement: {}\n'.format(document)
                            document_added = True

                        report+=report_sentence

            else:
                report+='{} is in {} but not in {}\n\n'.format(document, p1.projectName, p2.projectName)

        return report, results, accuracy, total, seenSentences, seenLabels

    def getKappa(self, results, accuracy, total):
        if total!=0:
            p0 = accuracy/total
        else:
            p0=0

        pe = 0
        # print(results)

        annotators = list(results.keys())

        pe_total = 0
        for tag in results[annotators[0]]:
            if tag in results[annotators[1]]:
                pe+=results[annotators[0]][tag]*results[annotators[1]][tag]
                pe_total+=results[annotators[0]][tag]
                pe_total+=results[annotators[1]][tag]

        if pe_total!=0:
            pe/=(pe_total*pe_total)
            kappa = (p0-pe)/(1-pe)
        else:
            kappa=0

        return kappa, p0, pe 
