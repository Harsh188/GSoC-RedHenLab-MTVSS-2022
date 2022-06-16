# Copyright (c) 2022 Harshith Mohan Kumar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# =============================================================================

# Imports

class Model:
	"""
	This Model class is used to manage all of the classification models 
	and output of data related to the stage one of the pipeline. 
	Various methods are provided to retrieve, manipulate and store data.
	"""

	def __init__(self):
		pass

	def csv_merger(self,dir_path:str) -> str:
		'''Method to merge multiple csv outputs into one output.
		
		Args:
			dir_path (str): Path to where all the to be merged csv files exist.

		Returns:
			file_path (str): Path to merged csv file.
		'''
		pass

	def music_classification(self, files):
		'''Method to take batches of mp4 files, break them into 45min segments
		and segment them into noise/music/speech intervals.

		Args:
			
		Returns: 
		'''
		
		# Break file into 45min segments:

		# Feed segments into InaSpeechSegmenter (parallely)

		# Merge csv outputs

		pass