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
import pickle
from copy import deepcopy
import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from probabilisticassistant import ProbabilisticAssistant
import matplotlib.pyplot as plt

from pdb import set_trace


class GuiSupervisedLabeler():
	def __init__(self, gui, cocotaProject):
		self.project = cocotaProject

		self.GUI = gui
		self.output_directory = self.project.directory+'/output/'

		self.SKIP = "<SKIPPED>"
		self.mode = "Regular"

		self.seenAndUpdated = False

		self.back_old_tag = None
		# self.input_labels_dict_mirror = deepcopy(self.project.input_labels_dict)

	def labelNewSet(self):
		self.mode = "Regular"
		self.GUI.tag_labelingMode.setText("Regular")

		if len(self.project.input_labels_dict) == 0:
			self.project.current_schedule = list(self.project.input_sequences_dict.keys())[0]
			self.project.current_activity_index = 0		
		
		#### finish loading previous information
		##################################################################################
		if self.project.current_schedule not in self.project.input_labels_dict:
			self.project.input_labels_dict[self.project.current_schedule] = {}

		self.schedules = list(self.project.input_sequences_dict.keys())
		self.project.current_schedule_index = self.schedules.index(self.project.current_schedule)
		
		self.current_activity = self.project.input_sequences_dict[self.project.current_schedule][str(self.project.current_activity_index)]
		self.project.current_token_index = 0
		self.current_token = self.current_activity[self.project.current_token_index]

		self.project.current_prediction = self.project.probabilisticAssistant.predict(self.current_activity, self.project.current_token_index)

		self.project.current_labels = []

		self.updateGui()
		self.project.save()

	def getButtonText(self, buttonText):
		#receives which button is clicked
		# print(self.back_old_tag)
		# print(self.__dict__)

		self.project.current_tag = self.get_tag_from_gui(buttonText)

		if (self.project.current_tag in self.project.tags or 
			self.project.current_tag in ["Conjunction", "Preposition"]):

			if self.mode == "Regular":
				self.project.current_labels.append(self.project.current_tag)
				self.updateState()
				self.updateGui()
				self.back_old_tag = None

			if self.mode == "Review":
				self.project.review_labels.append(self.project.current_tag)
				self.updateStateReview()
				self.updateGuiReview()		

			if self.mode == "Modify":
				self.project.input_labels_dict[self.modified_schedule][self.modified_activity_index][self.modified_token_index]=self.project.current_tag
				for doc in self.project.input_labels_dict:
					doc_ = self.project.input_labels_dict[doc]
					for sent in doc_:
						sent_ = doc_[sent]
						if sent_ == self.modified_activity:
							old_label = deepcopy(self.input_labels_dict[doc][sent][self.modified_token_index])
							self.input_labels_dict[doc][sent][self.modified_token_index] = self.project.current_tag
							self.updatePA(self.modified_activity, self.input_labels_dict[doc][sent], self.modified_token_index, old_label=None)

				self.close_annotaiton_window()
				msg = QMessageBox()
				msg.setText("Labels for all similar tokens have been updated successfully.")
				msg.exec_()
				

			if self.mode == "Skipped":
				self.project.skipped_labels[self.project.skipped_token_index] = self.project.current_tag
				self.updateStateSkipped()
				self.updateGuiSkipped()
				pass
		else:
			msg = QMessageBox()
			msg.setText("No prediction was made, please choose one of the labels instead...")
			msg.exec_()


	def updatePA(self, activity, labels, token_index, old_label=None):
		# print('updating PA')

		if labels[token_index]!=self.SKIP:
			if old_label != None:
				self.project.probabilisticAssistant.update(activity, token_index, labels[token_index], old_tag=old_label)
			else:	
				self.project.probabilisticAssistant.update(activity, token_index, labels[token_index])


	def updateState(self, skipping=False):
		# print("labels", self.project.current_labels)
		if skipping==False:
			# print(self.current_activity, self.project.current_labels, self.project.current_token_index)
			if len(self.project.current_labels)>0:
				# if len(self.project.current_labels)>=self.project.current_token_index+1:
				if self.back_old_tag != None:
					self.updatePA(self.current_activity, self.project.current_labels, self.project.current_token_index, self.back_old_tag)
				else:
					self.updatePA(self.current_activity, self.project.current_labels, self.project.current_token_index)
		
		if self.project.current_token_index == len(self.current_activity)-1: # and len(self.current_activity)>1:
			self.project.seen_acts[str(self.current_activity)] = self.project.current_labels
			# if it's the last token in the activity

			if self.project.current_activity_index < len(self.project.input_sequences_dict[self.project.current_schedule])-1:
				# if the activity is not the last activity in the schedule

				self.project.input_labels_dict[self.project.current_schedule][str(self.project.current_activity_index)] = self.project.current_labels
				self.project.current_activity_index +=1
				self.current_activity = self.project.input_sequences_dict[self.project.current_schedule][str(self.project.current_activity_index)]
				self.project.current_token_index = 0
				self.current_token = self.current_activity[self.project.current_token_index]
				self.project.current_labels = []
				if self.seenAndUpdated:
					self.updateState()

			else:
				# if the activity is the last activity in the schedule:
				if self.project.current_schedule_index == len(self.project.input_sequences_dict)-1:
					#if the schedule is the last schedule in the input dict:
					
					# if self.project.input_sequences_dict[self.project.current_schedule][str(self.project.current_activity_index)] == self.current_activity:
					self.project.input_labels_dict[self.project.current_schedule][str(self.project.current_activity_index)] = self.project.current_labels					
					self.project.save()
					msg = QMessageBox()
					msg.setText("There are no more sentences to annotate in the uploaded documents.")
					msg.exec_()
					self.close_annotaiton_window()
					return

				else:
					# if there are more schedules to annotate:
					# add the new schedule to the labels dict and start from the activity at 0
					self.project.current_schedule_index+=1
					self.project.current_schedule = list(self.project.input_sequences_dict.keys())[self.project.current_schedule_index]
					
					if self.project.current_schedule not in self.project.input_labels_dict:
						self.project.input_labels_dict[self.project.current_schedule] = {}

					self.project.current_activity_index = 0
					self.current_activity = self.project.input_sequences_dict[self.project.current_schedule][str(self.project.current_activity_index)]
					self.project.current_token_index = 0
					self.current_token = self.current_activity[self.project.current_token_index]
					self.project.current_labels = []
					self.seenAndUpdated = False

		
		elif self.project.current_token_index == 0:
			# if the new activity is already seen, retreive the labels and recall the function
			if str(self.current_activity) in self.project.seen_acts:
				self.project.current_labels = self.project.seen_acts[str(self.current_activity)]
				self.project.input_labels_dict[self.project.current_schedule][self.project.current_activity_index] = self.project.current_labels					
				self.project.current_token_index=len(self.current_activity)-1
				self.seenAndUpdated = True
				self.updateState()
			
			else:
				self.seenAndUpdated = False
				if len(self.project.current_labels)==0:
					pass
				else:
					if len(self.current_activity)==1:
						self.project.input_labels_dict[self.project.current_schedule][str(self.project.current_activity_index)] = self.project.current_labels
						self.project.current_activity_index +=1
						self.current_activity = self.project.input_sequences_dict[self.project.current_schedule][str(self.project.current_activity_index)]
						self.project.current_token_index = 0
						self.current_token = self.current_activity[self.project.current_token_index]
						self.project.current_labels = []
					else:
						self.project.current_token_index+=1
						self.current_token = self.current_activity[self.project.current_token_index]

		else:
			# if there are more tokens in the current activity
			self.seenAndUpdated = False
			self.project.current_token_index+=1
			self.current_token = self.current_activity[self.project.current_token_index]

		# if the new token in a preposition or a conjuction, add it to the labels and
		# call this function again
		if self.current_token in ['and', '&', 'or', 'but', 'nor', 'yet', 'so', 'for']:
			self.project.current_labels.append('Conjunction')
			self.updateState()
		
		elif self.current_token in ['at', 'from', 'to', 'into', 'until', 'through',   # "in" might appear as part of rough in #'on' might appear in slab on grade
					 'under', 'above', 'near', 'by','towards', 'across', 'along',
					 'about', 'behind','beyond', 'between', 'within', 'around']:	 
			self.project.current_labels.append('Preposition')
			self.updateState()
		


		# predict the new label
		self.project.current_prediction = self.project.probabilisticAssistant.predict(self.current_activity, self.project.current_token_index)
		self.project.save()

	def review(self, reviewd_activities=0):
		if len(self.project.repeat_list)==0:
			msg = QMessageBox()
			msg.setText("No previous activities were found for review...")
			msg.exec_()
			self.close_annotaiton_window()
			return False

		else:
			self.project.review_schedule, self.project.review_activity_index = self.project.repeat_list[-1]
			if self.project.review_schedule in self.project.input_labels_dict:
				if str(self.project.review_activity_index) in self.project.input_labels_dict[self.project.review_schedule]:
					reviewd_activities+=1
					self.mode = "Review"
					self.GUI.tag_labelingMode.setText("Review")

					self.review_activity = self.project.input_sequences_dict[self.project.review_schedule][str(self.project.review_activity_index)]
					self.project.review_token_index = 0
					self.project.current_prediction = self.project.probabilisticAssistant.predict(self.review_activity, self.project.review_token_index)
					self.project.review_labels=[] 
					self.updateGuiReview()
					self.project.save()

				else:
					msg = QMessageBox()
					msg.setText("One of the activities in the revision list hasn't been labeled yet. It will be skipped...")
					msg.exec_()
					self.project.repeat_list.pop()
					self.review(reviewd_activities)

			else:
				msg = QMessageBox()
				msg.setText("One of the activities in the revision list hasn't been labeled yet. It will be skipped...")
				msg.exec_()
				self.project.repeat_list.pop()
				self.review(reviewd_activities)
		
		if reviewd_activities > 0:
			return True
		else:
			return False

	def updateStateReview(self):
		# self.project.probabilisticAssistant.update(self.review_activity, self.project.review_token_index, self.project.current_tag)
		# self.project.save()

		# set_trace()
		previous_labels = self.project.input_labels_dict[self.project.review_schedule][str(self.project.review_activity_index)]
		self.updatePA(self.review_activity, self.project.review_labels, self.project.review_token_index, previous_labels[self.project.review_token_index])

		# print(self.project.repeat_list)
		if self.project.review_token_index == len(self.review_activity)-1:

			# previous_labels = self.project.input_labels_dict[self.project.review_schedule][str(self.project.review_activity_index)]
			# self.updatePA(self.review_activity, self.project.review_labels, self.project.review_token_index,  old_label=previous_labels[self.project.review_token_index])

			self.project.input_labels_dict[self.project.review_schedule][str(self.project.review_activity_index)] = self.project.review_labels
			self.project.seen_acts[str(self.review_activity)] = self.project.review_labels

			# checking and updating all similar activities
			for labeled_activiy_index in self.project.input_labels_dict[self.project.review_schedule]:
				labeled_activiy = self.project.input_labels_dict[self.project.review_schedule][labeled_activiy_index]
				if str(self.review_activity) == str(labeled_activiy):
					self.project.input_labels_dict[self.project.review_schedule][labeled_activiy_index] = self.project.review_labels
					check_tuple = (self.project.review_schedule_index, labeled_activiy_index)
					if check_tuple in self.project.repeat_list:
						self.project.repeat_list.remove(check_tuple)
			# checking and updating all similar activities

			self.project.review_labels = []

			if len(self.project.repeat_list)>1:
				self.project.repeat_list.pop()
				self.project.review_schedule, self.project.review_activity_index = self.project.repeat_list[-1]
				self.project.review_token_index=0

			elif len(self.project.repeat_list)==1:
				self.project.repeat_list.pop()
				msg = QMessageBox()
				msg.setText("There are no more activities available for review...")
				msg.exec_()
				self.close_annotaiton_window()

		else:
			self.project.review_token_index+=1

		self.project.current_prediction = self.project.probabilisticAssistant.predict(self.review_activity, self.project.review_token_index)
		self.project.save()


	def updateStateSkipped(self):
		self.updatePA(self.skipped_activity, self.project.skipped_labels, self.project.skipped_token_index)
		self.project.input_labels_dict[self.project.skipped_schedule][str(self.skipped_activity_index)] = self.project.skipped_labels
		self.project.seen_acts[str(self.skipped_activity)] = self.project.skipped_labels

		# checking and updating all similar activities
		for labeled_activiy_index in self.project.input_labels_dict[self.project.skipped_schedule]:
			labeled_activiy = self.project.input_labels_dict[self.project.skipped_schedule][labeled_activiy_index]
			if str(self.skipped_activity) == str(labeled_activiy):
				self.project.input_labels_dict[self.project.skipped_schedule][labeled_activiy_index] = self.project.skipped_labels
				check_tuple = (self.project.skipped_schedule_index, labeled_activiy_index, self.project.skipped_token_index)
				if check_tuple in self.project.skip_list:
					self.project.skip_list.remove(check_tuple)
		# checking and updating all similar activities

		if len(self.project.skip_list) == 0:
			msg = QMessageBox()
			msg.setText("No previously skipped activities were found for review...")
			msg.exec_()
			self.close_annotaiton_window()

		else:
			self.project.skipped_schedule_index, self.skipped_activity_index, self.project.skipped_token_index = self.project.skip_list.pop()
			self.project.skipped_schedule = list(self.project.input_sequences_dict.keys())[self.project.skipped_schedule_index]
			self.skipped_activity = self.project.input_sequences_dict[self.project.skipped_schedule][str(self.skipped_activity_index)]
			self.project.current_prediction = self.project.probabilisticAssistant.predict(self.skipped_activity, self.project.skipped_token_index)
			self.project.skipped_labels= self.project.input_labels_dict[self.project.skipped_schedule][str(self.skipped_activity_index)] 

		self.project.save()

	def modify(self, document_index, sentence_index, token_index):
		sentence_index = str(sentence_index)
		documents_list = list(self.project.input_labels_dict.keys())
		
		msg = QMessageBox()

		if document_index < len(documents_list):
			document = documents_list[document_index]
		else:
			msg.setText("There is no document at this index. Please choose one of the available documents from the list.")
			msg.exec_()
			self.close_annotaiton_window()
			return

		if sentence_index in self.project.input_sequences_dict[document]:
			sentence = self.project.input_sequences_dict[document][sentence_index]
		else:
			msg.setText("The provided sentence index is not valid.")
			msg.exec_()
			self.close_annotaiton_window()
			return

		if token_index < len(sentence):
			token = sentence[token_index]
		else:
			msg.setText("The provided token index is not valid.")
			msg.exec_()
			self.close_annotaiton_window()
			return

		try:
			current_label = self.project.input_labels_dict[document][sentence_index][token_index]
		
		except:
			msg.setText("The designated token hasn't been previously annotated.")
			msg.exec_()
			self.close_annotaiton_window()
			return

		self.mode = 'Modify'
		self.GUI.tag_labelingMode.setText("Modify")

		self.modified_schedule_index = document_index
		self.modified_schedule = document
		self.modified_activity_index = sentence_index
		self.modified_activity = sentence
		self.modified_token_index = token_index
		self.modified_current_label = current_label

		self.updateGuiModify()


	def labelSkipped(self):
		self.project.skip_list = []
		for sch_ind, sch in enumerate(self.project.input_labels_dict):
			for act_index in self.project.input_labels_dict[sch]:
				for i, label in enumerate(self.project.input_labels_dict[sch][act_index]):
					if label == self.SKIP:
						self.project.skip_list.insert(0, (sch_ind, int(act_index), i))


		if len(self.project.skip_list) == 0:
			msg = QMessageBox()
			msg.setText("No previously skipped activities were found for review...")
			msg.exec_()
			return False

		else:
			self.mode = 'Skipped'
			self.GUI.tag_labelingMode.setText("Skipped")
			
			self.project.skipped_schedule_index, self.skipped_activity_index, self.project.skipped_token_index = self.project.skip_list.pop()
			self.project.skipped_schedule = list(self.project.input_sequences_dict.keys())[self.project.skipped_schedule_index]
			self.skipped_activity = self.project.input_sequences_dict[self.project.skipped_schedule][str(self.skipped_activity_index)]
			self.project.current_prediction = self.project.probabilisticAssistant.predict(self.skipped_activity, self.project.skipped_token_index)
			self.project.skipped_labels= self.project.input_labels_dict[self.project.skipped_schedule][str(self.skipped_activity_index)] 
			self.updateGuiSkipped()
		self.project.save()

		return True	

	def updateGui(self):
		self.GUI.tag_schedleInformation.setText(self.project.current_schedule)
		self.GUI.tag_token.setText(self.current_token)

		self.GUI.tag_activity.setText(" ".join(self.current_activity))
		# self.GUI.tag_activity.insertPlainText(" ".join(self.current_activity))
		
		self.GUI.tag_activityIndex.setText(str(self.project.current_activity_index))
		# print("current Prediciton: {}".format(self.project.current_prediction))
		self.GUI.tag_suggestion.setText(self.project.current_prediction)
		
		if not self.GUI.button_addToReview.isEnabled():
			self.GUI.button_addToReview.setEnabled(True)

		if not self.GUI.button_skip.isEnabled():
			self.GUI.button_skip.setEnabled(True)

		if (self.project.current_prediction not in self.project.tags and 
			self.project.current_prediction not in ["Conjunction", "Preposition"]):
			self.GUI.button_acceptPrediction.setEnabled(False)
			self.GUI.button_stats.setEnabled(False)
		else:
			if not self.GUI.button_acceptPrediction.isEnabled():
				self.GUI.button_acceptPrediction.setEnabled(True)
			if not self.GUI.button_stats.isEnabled():
				self.GUI.button_stats.setEnabled(True)

		if self.project.current_schedule_index==0 and self.project.current_activity_index==0 and self.project.current_token_index == 0:
			self.GUI.button_back.setEnabled(False)
		else:
			if not self.GUI.button_back.isEnabled():	
				self.GUI.button_back.setEnabled(True)

		self.GUI.annotationWindow.repaint()

	def updateGuiReview(self):
		if self.GUI.button_back.isEnabled():
			self.GUI.button_back.setEnabled(False)
			self.GUI.button_addToReview.setEnabled(False)

		if not self.GUI.button_skip.isEnabled():
			self.GUI.button_skip.setEnabled(True)

		if (self.project.current_prediction not in self.project.tags and 
			self.project.current_prediction not in ["Conjunction", "Preposition"]):
			self.GUI.button_acceptPrediction.setEnabled(False)
			self.GUI.button_stats.setEnabled(False)
		else:
			if not self.GUI.button_acceptPrediction.isEnabled():
				self.GUI.button_acceptPrediction.setEnabled(True)
			if not self.GUI.button_stats.isEnabled():
				self.GUI.button_stats.setEnabled(True)

		self.GUI.tag_schedleInformation.setText(self.project.review_schedule)
		self.GUI.tag_token.setText(self.review_activity[self.project.review_token_index])
		self.GUI.tag_activity.setText(" ".join(self.review_activity))
		self.GUI.tag_activityIndex.setText(str(self.project.review_activity_index))
		self.GUI.tag_suggestion.setText(self.project.current_prediction)
		self.GUI.annotationWindow.repaint()

	def updateGuiSkipped(self):
		if self.GUI.button_back.isEnabled():
			self.GUI.button_back.setEnabled(False)

		if not self.GUI.button_skip.isEnabled():
			self.GUI.button_skip.setEnabled(True)

		if (self.project.current_prediction not in self.project.tags and 
			self.project.current_prediction not in ["Conjunction", "Preposition"]):
			self.GUI.button_acceptPrediction.setEnabled(False)
			self.GUI.button_stats.setEnabled(False)
		else:
			if not self.GUI.button_acceptPrediction.isEnabled():
				self.GUI.button_acceptPrediction.setEnabled(True)
			if not self.GUI.button_stats.isEnabled():
				self.GUI.button_stats.setEnabled(True)

		self.GUI.tag_schedleInformation.setText(self.project.skipped_schedule)
		self.GUI.tag_token.setText(self.skipped_activity[self.project.skipped_token_index])
		self.GUI.tag_activity.setText(" ".join(self.skipped_activity))
		self.GUI.tag_activity.adjustSize()
		self.GUI.tag_activityIndex.setText(str(self.skipped_activity_index))
		self.GUI.tag_suggestion.setText(self.project.current_prediction)
		self.GUI.annotationWindow.repaint()

	def updateGuiModify(self):
		self.GUI.button_acceptPrediction.setEnabled(False)
		self.GUI.button_addToReview.setEnabled(False)
		self.GUI.button_back.setEnabled(False)
		self.GUI.button_skip.setEnabled(False)
		self.GUI.tag_suggestion_fixed.setText("Current Label:")
		self.GUI.tag_suggestion.setText(self.modified_current_label)
		self.GUI.tag_schedleInformation.setText(self.modified_schedule)
		self.GUI.tag_activity.setText(" ".join(self.modified_activity))
		self.GUI.tag_activityIndex.setText(self.modified_activity_index)
		self.GUI.tag_token.setText(self.modified_activity[self.modified_token_index])
		self.GUI.annotationWindow.repaint()

	def get_tag_from_gui(self, buttonText):
		if buttonText == 'Accept Prediction':
			return self.project.current_prediction

		else:
			for tag in self.project.tags:
				if buttonText == tag:
					return tag


	def addCurrentActivityToReviewList(self):
		
		# if self.project.current_activity_index in self.project.input_labels_dict[self.project.current_schedule]:
		self.project.repeat_list.append((self.project.current_schedule, self.project.current_activity_index))
		self.project.save()
		# print(self.project.repeat_list)
		msg = QMessageBox()
		msg.setText("Current activity added to review list")
		msg.exec_()

		# else:
		# 	msg.setText("This activity hasn't been labeled yet")
			# msg.exec_()

	
	def skip(self):	
		self.project.current_labels.append(self.SKIP)
		self.updateState(skipping=True)
		self.updateGui()


	def plot_stats(self):
		if self.mode == "Regular":
			stats_token = self.current_token
		elif self.mode == "Review":
			stats_token = self.review_activity[self.project.review_token_index]
		elif self.mode == "Skipped":
			stats_token = self.skipped_activity[self.project.skipped_token_index]
		elif self.mode == "Modify":
			stats_token = self.modified_activity[self.modified_token_index]
		else:
			return

		stats_dict = self.project.probabilisticAssistant.unigrams[stats_token]
		# print(stats_dict)
		X = list(stats_dict.keys())
		Y = [stats_dict[x] for x in X]
		total = sum(Y)
		Y_ = [y/total*100 for y in Y]
		data = {"Total Count": total}
		fig = plt.bar(X, Y_, width=0.01, bottom=None, data=data)
		plt.xlabel('Potential Labels')
		plt.ylabel('Probability - Total Count: {}'.format(total))
		plt.title('Stats of \"{}\"'.format(stats_token))
		plt.show()


	def go_back(self):

		# self.input_labels_dict_mirror = deepcopy(self.project.input_labels_dict)
		
		if str(self.current_activity) in self.project.seen_acts:
			del self.project.seen_acts[str(self.current_activity)]

		if self.project.current_schedule_index==0:
			if self.project.current_activity_index==0:
				self.project.current_token_index-=1
				# old_tag = self.project.current_labels.pop() 
			else:
				if self.project.current_token_index==0:
					self.project.current_activity_index-=1
					self.current_activity = self.project.input_sequences_dict[self.project.current_schedule][str(self.project.current_activity_index)]
					self.project.current_token_index = len(self.current_activity)-1
					self.project.current_labels = self.project.input_labels_dict[self.project.current_schedule][str(self.project.current_activity_index)]
					# old_tag = self.project.current_labels.pop()
				
				else:
					self.project.current_token_index-=1
					 # old_tag = self.project.current_labels.pop() 	

		else:
			if self.project.current_activity_index==0:
				if self.project.current_token_index == 0:
					self.project.current_schedule_index-=1
					self.project.current_schedule = list(self.project.input_sequences_dict.keys())[self.project.current_schedule_index]
					self.project.current_activity_index = len(self.project.input_sequences_dict[self.project.current_schedule])-1
					self.current_activity = self.project.input_sequences_dict[self.project.current_schedule][str(self.project.current_activity_index)]
					self.project.current_token_index = len(self.current_activity)-1

					self.project.current_labels = self.project.input_labels_dict[self.project.current_schedule][str(self.project.current_activity_index)]
					# old_tag = self.project.current_labels.pop()

				else:
					self.project.current_token_index-=1
					# old_tag = self.project.current_labels.pop() 
			else:
				if self.project.current_token_index==0:
					self.project.current_activity_index-=1
					self.current_activity = self.project.current_schedule[str(self.project.current_activity_index)]
					self.project.current_token_index = len(self.current_activity)-1
					self.project.current_labels = self.project.input_labels_dict[self.project.current_schedule][str(self.project.current_activity_index)]
					# old_tag = self.project.current_labels.pop()
				
				else:
					self.project.current_token_index-=1

		self.current_token = self.current_activity[self.project.current_token_index]
		self.project.current_prediction = self.project.probabilisticAssistant.predict(self.current_activity, self.project.current_token_index)
			
		self.get_relevant_old_label()
		self.project.current_labels.pop()

		self.updateGui()

	def get_relevant_old_label(self):
		if self.project.current_activity_index in self.project.input_labels_dict[self.project.current_schedule]:
			labels = self.project.input_labels_dict[self.project.current_schedule][self.project.current_activity_index]
			self.back_old_tag = labels[self.project.current_activity_index]
		
		else:
			self.back_old_tag = deepcopy(self.project.current_labels[-1])

	def close_annotaiton_window(self):
		self.GUI.mainWindowForm.show()
		self.GUI.annotationWindow.close()