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

import os
import glob

import pandas as pd
import numpy as np

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import constants as const

class Data:
	"""
	This Data class is used to manage all of the ingestion
	and output of data related to the stage one of the pipeline.
	Various methods are provided to retrieve, manipulate and store data.
	"""

	def __init__(self, job_num:int, verbose:bool,file_path):
		self.job_num = job_num
		self.verbose = verbose
		self.file_path = file_path

	def ingestion(self) -> np.ndarray:
		"""The ingestion method is used to pull in all the mp4 files 
		related to a certain category. The files are stored in batches
		and based on the Array job number, the corresponding batch is returned.
		
		Args:
			category (str): TODO
		Returns:
			batches (List): List of mp4 files.
		"""

		batch_path = self.file_path+"/hxm471/mtvss/data/tmp/batch_cat1.npy"
		# Check if Batched file exists
		if(not os.path.isfile(batch_path)):
			raise Exception("Batch file {0} does not exist!".format(batch_path))
		else:
			batches = np.load(batch_path, allow_pickle=True)
			return batches[self.job_num]
		pass