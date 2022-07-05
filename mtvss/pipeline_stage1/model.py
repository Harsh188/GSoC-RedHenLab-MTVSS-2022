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

sys.path.insert(1,'/tmp/hxm471/inaSpeechSegmenter')
from segmenter import Segmenter, seg2csv

class Model:
	"""
	This Model class is used to manage all of the classification models 
	and output of data related to the stage one of the pipeline. 
	Various methods are provided to retrieve, manipulate and store data.
	"""

	def __init__(self,file,verbose):
		self.file=file
		self.verbose=verbose
		self.segments=[]
		pass

	def music_classification(self):
		'''Method to invoke InaSpeechSegmenter and produce segments of
		noise/music/speech intervals.
		'''

		if(self.verbose):
			print("\n-- Step 2.1.1: Initializing Segmenter --\n")
		# Initialize the segmenter
		seg = Segmenter(vad_engine=const.VAD_ENGINE, detect_gender=const.DETECT_GENDER, 
				ffmpeg=const.FFMPEG_BINARY, energy_ratio=const.ENERGY_RATIO, 
				batch_size=const.BATCH_SIZE)
		if(self.verbose):
			print("\n-- Step 2.1.2: Checking output directory --\n")
		# Check output DIR
		odir = const.TMP_PATH+'splits'
		assert os.access(odir, os.W_OK), 'Directory %s is not writable!' % odir


		with warnings.catch_warnings():
			warnings.simplefilter("ignore")

			# Extract basename of file
			base = [os.path.splitext(os.path.basename(self.file))]
			output_files = [os.path.join(odir, e + '.' + 'csv') for e in base]

			if(self.verbose):
				print("\nbase files:\n",base)
				print("\nOutput files:\n",output_files)
				print("\n-- Step 2.1.3: Starting batch process --\n")

			seg.batch_process(self.files.tolist(), output_files, 
				verbose=self.verbose, output_format='csv')
		return