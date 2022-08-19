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

	def get_drop_indices(csv_file_path:str) -> np.ndarray:
		"""This method is a preprocessing filter to extract only images
			which meet a certain standard for further cluster. It useses the 
			confidence values and the duration of the clips to determine if
			the images from that section should be used or dropped.

		Args:
			csv_file_path (str): Path of the csv with metadata on image features.
		Returns:
			drop_indices (np.noarray): List of indices to drop from the npy file
		"""
		# Initialize variable to store drop indices
		drop_indices=None
		# Read csv and store as a DataFrame
		df = pd.read_csv(csv_file_path)
		# Get indices of low confidence values
		df = df['confidence'] < 0.95
		# Get indices of low delta time
		df.drop(df[df['end']-df['start'] >= 10].index, inplace=True)
		# Get indices of rows to remove
		drop_indices = df.index.unique()
		
		return drop_indices

	def get_clean_arrays(arr, file_path:str) -> np.ndarray:
		"""This method cleans the existing features by figuring out what indices
			to drop and then mapping it to the indicies of arrays in npy file.

		Args:
			arr (np.mmap): Binary file with features to filter
			csv_file_path (str): Path of the csv with metadata on image features.
		Returns:
			final_arr (np.ndarray): Numpy array containing final features to be used
				for clustering.
		"""
		csv_file_path = file_path[:-3]+'csv'
		drop_indices = get_drop_indices(csv_file_path)
		final_drop_indices = np.empty(0)
		for x in drop_indices:
			final_drop_indices = np.concatenate(final_drop_indices, [x,x+1,x+2,x+3,x+4], axis=1)

		if self.verbose:
			print('\n---- Preprocessing ----\n')
			print("## Number of features dropped:", final_drop_indices-final_drop_indices)

		final_arr = np.delete(arr, final_drop_indices)

		return final_arr

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
			# Appened appropriate features
			data.append(get_clean_arrays(np.load(f,mmap_mode='r'),f))
			ctr+=1
			# print(data.shape)
		data_arr = np.concatenate(data,axis=0)
		print(data_arr.shape)
		mmap_path = self.file_path+'/final_data.npy' 
		np.save(mmap_path,data_arr)
		data_mmap = np.load(mmap_path,mmap_mode='r')
		return data_mmap

	def optimization_ingestion(self) -> np.ndarray:
		"""Data ingestion method to load in image features into memory using
		mmap mode. Unlike the regular ingestion method this one loads in a subset
		which is used to tune the number of neighbors paramter for the RNN-DBSCAN.
		
		Args:
			file (str): Current directory path in string format.
		Returns:
			data (List): List of image features loaded in mmap_mode.
							Contains shape (#image_features, feature_size)
		"""
		if self.verbose:
			print("\n --- Optimization Data Ingestion ---\n")

		# Initialize list to store array of mmaps
		data = []

		# Year and day to look for in iter 1
		loop_1_year = '1996'
		loop_1_day = '02'

		ctr=0
		for f in glob.glob(const.SCRATCH_PATH+'tmp/'+loop_1_year+'*'+loop_1_day+'*image_features*.npy'):
			# data.append(np.load(f,mmap_mode='r'))
			data.append(get_clean_arrays(np.load(f,mmap_mode='r'),f))
			ctr+=1

		# Year and day to look for in iter 2
		loop_1_year = '2001'
		loop_1_day = '07'

		ctr=0
		for f in glob.glob(const.SCRATCH_PATH+'tmp/'+loop_1_year+'*'+loop_1_day+'*image_features*.npy'):
			# data.append(np.load(f,mmap_mode='r'))
			data.append(get_clean_arrays(np.load(f,mmap_mode='r'),f))
			ctr+=1

		data_arr = np.concatenate(data,axis=0)
		print(data_arr.shape)
		mmap_path = self.file_path+'/final_data.npy' 
		np.save(mmap_path,data_arr)
		data_mmap = np.load(mmap_path,mmap_mode='r')
		return data_mmap

		if self.verbose:
			print("## Number of files ingested:",ctr)
