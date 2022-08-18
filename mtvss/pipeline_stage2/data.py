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
		"""Data ingestion method to load in image features into memory using
		mmap mode. All files binary files in the /scratch directory are loaded
		and concatenated as an np.array with shape (#image_features, feature_size)
		where feature_size = 2048.
		
		Args:
			file (str): Current directory path in string format.
		Returns:
			data (List): List of image features loaded in mmap_mode.
							Contains shape (#image_features, feature_size)
		"""
		# data = np.empty((0,2048))
		data = []
		ctr = 0
		for f in glob.glob(const.SCRATCH_PATH+'tmp/'+'*image_features*.npy'):
			# data = np.append(data,np.load(f,mmap_mode='r'),axis=0)
			data.append(np.load(f,mmap_mode='r'))
			ctr+=1
			# print(data.shape)
		data_arr = np.concatenate(data,axis=0)
		print(data_arr.shape)
		mmap_path = self.file_path+'/final_data.npy' 
		np.save(mmap_path,data_arr)
		data_mmap = np.load(mmap_path,mmap_mode='r')
		return data_mmap