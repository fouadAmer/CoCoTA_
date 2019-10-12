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

from guisupervisedlabeler import GuiSupervisedLabeler
from probabilisticassistant import ProbabilisticAssistant
from PyQt5.QtWidgets import QMessageBox
from copy import deepcopy
from collections import defaultdict

import pickle, json

class Cocota:
	def __init__(self):
		self.fileExtension = '.cocota'
		self.projectName = None
		self.directory = None

		self.probabilisticAssistant = ProbabilisticAssistant()

		self.input_sequences_dict = {}
		self.input_labels_dict = {}
		self.tags = {}

		self.seen_acts = {}
		self.skip_list = []
		self.repeat_list = []

		# regular annotations status
		self.current_schedule = None
		self.current_schedule_index = None
		self.current_activity_index = None
		self.current_token_index = None
		self.current_labels = []

		# review status
		self.review_schedule = None
		self.review_schedule_index = None
		self.review_activity_index = None
		self.review_token_index = None
		self.review_labels = []

		# skipped status
		self.skipped_schedule = None
		self.skipped_schedule_index = None
		self.skipped_activity_index = None
		self.skipped_token_index = None
		self.skipped_labels = []

		self.current_prediction = None		
		self.current_tag = None


	def save(self):
		save_dict = deepcopy(self.__dict__)
		assistant = self.getAssistantDict()
		save_dict["probabilisticAssistant"] = assistant
		
		with open ("{}/{}.cocota".format(self.directory,self.projectName) , 'wb') as outfile:
			pickle.dump(save_dict, outfile, protocol = pickle.HIGHEST_PROTOCOL)

		with open ("{}/{}_assistant.acocota".format(self.directory,self.projectName) , 'w') as outfile:
			json.dump(self.probabilisticAssistant.__dict__, outfile)

	
	def getAssistantDict(self):
		assistant = {}
		assistant["unigrams"] = dict(self.probabilisticAssistant.unigrams)
		assistant["bigrams"] = dict(self.probabilisticAssistant.bigrams)
		assistant["trigrams"] = dict(self.probabilisticAssistant.trigrams)
		assistant["bigramSurroundings"] = dict(self.probabilisticAssistant.bigramSurroundings)
		assistant["trigramSurroundings"] = dict(self.probabilisticAssistant.trigramSurroundings)
		return assistant

	def load(self, fileDirectory):
		if fileDirectory!='':
			try:
				with open (fileDirectory, 'rb') as infile:
					self.__dict__ = pickle.load(infile)

				unigrams = defaultdict(lambda: defaultdict(int))
				bigrams = defaultdict(lambda: defaultdict(int))
				trigrams = defaultdict(lambda: defaultdict(int))
				bigramSurroundings = defaultdict(lambda: defaultdict(int))
				trigramSurroundings = defaultdict(lambda: defaultdict(int))

				dict_ = self.probabilisticAssistant["unigrams"]
				for key1 in dict_:
					for key2 in dict_[key1]:
						unigrams[key1][key2] = dict_[key1][key2]

				dict_ = self.probabilisticAssistant["bigrams"]
				for key1 in dict_:
					for key2 in dict_[key1]:
						bigrams[key1][key2] = dict_[key1][key2]

				dict_ = self.probabilisticAssistant["trigrams"]
				for key1 in dict_:
					for key2 in dict_[key1]:
						trigrams[key1][key2] = dict_[key1][key2]
				
				dict_ = self.probabilisticAssistant["bigramSurroundings"]
				for key1 in dict_:
					for key2 in dict_[key1]:
						bigramSurroundings[key1][key2] = dict_[key1][key2]

				dict_ = self.probabilisticAssistant["trigramSurroundings"]
				for key1 in dict_:
					for key2 in dict_[key1]:
						trigramSurroundings[key1][key2] = dict_[key1][key2]

				self.probabilisticAssistant = ProbabilisticAssistant()
				self.probabilisticAssistant.unigrams = unigrams
				self.probabilisticAssistant.bigrams = bigrams
				self.probabilisticAssistant.trigrams = trigrams
				self.probabilisticAssistant.bigramSurroundings = bigramSurroundings
				self.probabilisticAssistant.trigramSurroundings = trigramSurroundings
				
				return True

			except:
				msg = QMessageBox()
				msg.setText("The chosen file is not a native cocota project and it cannot be opened\nPlease choose another project.")
				msg.exec_()
				return False
		else:
			return False