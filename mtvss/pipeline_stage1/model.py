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
import glob
import os
import sys
import warnings

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import constants as const

from inaSpeechSegmenter import Segmenter, seg2csv

class Model:
	"""
	This Model class is used to manage all of the classification models 
	and output of data related to the stage one of the pipeline. 
	Various methods are provided to retrieve, manipulate and store data.
	"""

	def __init__(self,files,verbose):
		self.files=files
		self.verbose=verbose
		self.segments=[]
		pass

	def csv_merger(self,dir_path:str) -> str:
		'''Method to merge multiple csv outputs into one output.
		
		Args:
			dir_path (str): Path to where all the to be merged csv files exist.

		Returns:
			file_path (str): Path to merged csv file.
		'''
		pass

	def segment_file(self,file):
		'''
		'''

		# Check if file's segments exists
		if(os.path.isdir(const.TMP_PATH+
			file[const.FOLDER_START_INDEX:const.FILE_START_INDEX])):
			return
		else:
			os.system("ffmpeg -i {0} -c copy -map 0 "\
				"-segment_time 00:45:00 -f segment"\
				" {1}{2}_output%03d.mp4".format(file,const.TMP_PATH+'/splits/',
					file[const.FOLDER_START_INDEX:]))
		self.segments.append(const.TMP_PATH+'/splits/'+
					file[const.FOLDER_START_INDEX:const.FILE_START_INDEX])
		return

	def music_classification(self):
		'''Method to invoke InaSpeechSegmenter and produce segments of
		noise/music/speech intervals.

		Args:

		Returns: 
		'''

		if(self.verbose):
			print("\n-- Step 2.1: Initializing Segmenter --\n")
		# Initialize the segmenter
		seg = Segmenter(vad_engine=const.VAD_ENGINE, detect_gender=const.DETECT_GENDER, 
				ffmpeg=const.FFMPEG_BINARY, energy_ratio=const.ENERGY_RATIO, 
				batch_size=const.BATCH_SIZE)
		if(self.verbose):
			print("\n-- Step 2.2: Checking output directory --\n")
		# Check output DIR
		odir = const.TMP_PATH+'splits'
		assert os.access(odir, os.W_OK), 'Directory %s is not writable!' % odir


		with warnings.catch_warnings():
			warnings.simplefilter("ignore")

			# Extract basename of file
			base = [os.path.splitext(os.path.basename(e))[0] for e in self.files]
			output_files = [os.path.join(odir, e + '.' + 'csv') for e in base]

			if(self.verbose):
				print("\nbase files:\n",base)
				print("\nOutput files:\n",output_files)
				print("\n-- Step 2.3: Starting batch process --\n")

			seg.batch_process(self.files.tolist(), output_files, 
				verbose=self.verbose, output_format='csv')
		
		# Merge csv outputs

		pass