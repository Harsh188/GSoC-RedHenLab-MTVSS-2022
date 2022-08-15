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
	and output of data related to the stage two of the pipeline.
	Various methods are provided to retrieve, manipulate and store data.
	"""

	def __init__(self,verbose:bool,file_path):
		self.verbose = verbose
		self.file_path = file_path

	def check_exist(self, file:str):
		pass

	def ingestion(self) -> np.ndarray:
		"""
		
		Args:
			category (str): TODO
		Returns:
			data (List): List of image features loaded in mmap_mode.
		"""
		data = np.empty((0,2048))
		ctr = 0
		for f in glob.glob(const.SCRATCH_PATH+'tmp/'+'*image_features*.npy'):
			data = np.append(data,np.load(f,mmap_mode='r'),axis=0)
			print(data.shape)
			ctr+=1
			if ctr==20:
				break
		return data