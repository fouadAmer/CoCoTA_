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
from collections import defaultdict
import operator

class ProbabilisticAssistant():
	def __init__(self):
		self.unigrams = defaultdict(lambda: defaultdict(int))
		self.bigrams = defaultdict(lambda: defaultdict(int))
		self.trigrams = defaultdict(lambda: defaultdict(int))

		self.bigramSurroundings = defaultdict(lambda: defaultdict(int))
		self.trigramSurroundings = defaultdict(lambda: defaultdict(int))

	def update(self, activity, word_index, input_tag, old_tag=None):
		self.unigrams[activity[word_index]][input_tag]+=1
		if word_index >= 1:
			self.bigrams[str(activity[word_index-1:word_index+1]).strip('[]')][input_tag]+=1
			if word_index < len(activity)-1:
				self.bigramSurroundings[str(activity[word_index-1:word_index+2]).strip('[]')][input_tag]+=1

		if word_index >= 2:
			self.trigrams[str(activity[word_index-2:word_index+1]).strip('[]')][input_tag]+=1
			if word_index < len(activity)-2:
				self.trigramSurroundings[str(activity[word_index-2:word_index+3]).strip('[]')][input_tag]+=1

		if old_tag != None:
			# if old_tag not in self.unigrams[activity[word_index]]:
			# 	print("error in the old_tag")
			self.unigrams[activity[word_index]][old_tag]-=1
			
			if self.unigrams[activity[word_index]][old_tag] == 0:
				del self.unigrams[activity[word_index]][old_tag]

			if word_index >= 1:
				self.bigrams[str(activity[word_index-1:word_index+1]).strip('[]')][old_tag]-=1
				if word_index < len(activity)-1:
					self.bigramSurroundings[str(activity[word_index-1:word_index+2]).strip('[]')][old_tag]-=1

			if word_index >= 2:
				self.trigrams[str(activity[word_index-2:word_index+1]).strip('[]')][old_tag]-=1
				if word_index < len(activity)-2:
					self.trigramSurroundings[str(activity[word_index-2:word_index+3]).strip('[]')][old_tag]-=1

		# self.save()
		
	def predict(self, activity, word_index):
		if word_index >= 2:
			if str(activity[word_index-2:word_index+3]) in self.trigramSurroundings:
				vals = self.trigramSurroundings[str(activity[word_index-2:word_index+3]).strip('[]')]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			elif str(activity[word_index-1:word_index+2]) in self.bigramSurroundings:
				vals = self.bigramSurroundings[str(activity[word_index-1:word_index+2]).strip('[]')]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			elif str(activity[word_index-2:word_index+1]) in self.trigrams:
				vals = self.trigrams[str(activity[word_index-2:word_index+1]).strip('[]')]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			elif str(activity[word_index-1:word_index+1]) in self.bigrams:
				vals = self.bigrams[str(activity[word_index-1:word_index+1]).strip('[]')]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			elif str(activity[word_index]) in self.unigrams:
				vals = self.unigrams[activity[word_index]]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			else:
				return ''

		elif word_index >= 1:
			if str(activity[word_index-1:word_index+2]) in self.bigramSurroundings:
				vals = self.bigramSurroundings[str(activity[word_index-1:word_index+2]).strip('[]')]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			elif str(activity[word_index-1:word_index]) in self.bigrams:
				vals = self.bigrams[str(activity[word_index-1:word_index+1]).strip('[]')]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			elif str(activity[word_index]) in self.unigrams:
				vals = self.unigrams[activity[word_index]]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			else:
				return ''

		else:
			if str(activity[word_index]) in self.unigrams:
				vals = self.unigrams[activity[word_index]]
				tag = max(vals.items(), key=operator.itemgetter(1))[0]
				return tag

			else:
				return ''
