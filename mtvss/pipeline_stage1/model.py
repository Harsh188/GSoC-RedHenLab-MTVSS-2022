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



from decord import VideoReader
from decord import gpu 

class Model:
	"""
	This Model class is used to manage all of the classification models 
	and output of data related to the stage one of the pipeline. 
	Various methods are provided to retrieve, manipulate and store data.
	"""
	def __init__(self,file,verbose,file_path):
		self.file=file
		self.verbose=verbose
		self.segments=[]
		self.file_path=file_path
		sys.path.insert(1,self.file_path+'/hxm471/inaSpeechSegmenter')
		self.segmenter = __import__("segmenter")
		pass

	def music_classification(self):
		'''Method to invoke InaSpeechSegmenter and produce segments of
		noise/music/speech intervals.
		'''

		if(self.verbose):
			print("\n-- Step 2.1.1: Initializing Segmenter --\n")
		# Initialize the segmenter
		seg = self.segmenter.Segmenter(vad_engine=const.VAD_ENGINE, detect_gender=const.DETECT_GENDER, 
				ffmpeg=const.FFMPEG_BINARY, energy_ratio=const.ENERGY_RATIO, 
				batch_size=const.BATCH_SIZE)
		if(self.verbose):
			print("\n-- Step 2.1.2: Checking output directory --\n")
		# Check output DIR
		odir = '/scratch/users/hxm471/tmp'
		assert os.access(odir, os.W_OK), 'Directory %s is not writable!' % odir


		with warnings.catch_warnings():
			warnings.simplefilter("ignore")

			# Extract basename of file
			base = os.path.splitext(os.path.basename(self.file))
			output_files = [os.path.join(odir, base[0] + '.' + 'csv')]

			if(self.verbose):
				print("\nbase files:\n",base[0])
				print("\nOutput files:\n",output_files)
				print("\n-- Step 2.1.3: Starting batch process --\n")

			result = seg.batch_process([self.file_path+'/hxm471/video_files/'+base[0]+'.mp4'], output_files, 
				tmpdir=self.file_path,verbose=self.verbose, output_format='csv', skipifexist=False)
			assert result[0] == 0, "Batch Process Failed!"

		return 

	def keyframe_extraction(self):
		'''This method is used to extract keyframes from music intervals.
		It uses an open-source software called Decord to efficiently seek
		and retrieve frames for specified music intervals.

		Args:

		Returns:
		'''
		if(self.verbose):
			print("\n-- Step 3.1: Initializing Decord --\n")
		# Initialize the VideoReader
		# vr = VideoReader(self.file, ctx=gpu(0))
		# Get metadata
		pass