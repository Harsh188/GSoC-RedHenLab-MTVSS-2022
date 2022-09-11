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
import numpy as np
import pandas as pd

import os
import sys
import glob
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import constants as const

# Functions
def parseArgs():
	'''Processes arugments

	Returns: parser.parse_args(): Returns populated namespace 
	'''
	parser = argparse.ArgumentParser(description='Pipeline Stage 2')
	parser.add_argument("--verbose",help='Print verbose statements '\
		'to check the progress of the program')
	parser.add_argument("--file_path",metavar="-F",help='tmp file path')
	return parser.parse_args()

class Ingestion:
	'''Seperate script to load in all of the features and store it into a 
	binary file.
	'''

	def __init__(self,verbose:bool,file_path):
		self.verbose = verbose
		self.file_path = file_path

	def get_drop_indices(self, csv_file_path:str) -> np.ndarray:
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
		# if self.verbose:
		# 	print("## Orig DF:",df)
		
		# Get indices of low confidence values
		df_filter = df['confidence'] < 0.95
		df = df.loc[df_filter]
		
		# Get indices of low and very high delta time
		df.drop(df[df['end']-df['start'] < 10].index, inplace=True)
		df.drop(df[df['end']-df['start'] > 100].index, inplace=True)
		
		# Get indices of commercials
		df.drop(df[df['label'] == 'TitleSequence'].index, inplace=True)
		
		# if self.verbose:
		# 	print("## Filtered DF:",df)
		
		# Get indices of rows to remove
		drop_indices = df.index.unique()
		
		return drop_indices

	def get_clean_arrays(self, arr, file_path:str) -> np.ndarray:
		"""This method cleans the existing features by figuring out what indices
			to drop and then mapping it to the indicies of arrays in npy file.

		Args:
			arr (np.mmap): Binary file with features to filter
			csv_file_path (str): Path of the csv with metadata on image features.
		Returns:
			final_arr (np.ndarray): Numpy array containing final features to be used
				for clustering.
		"""
		csv_file_path = file_path[:-12]+'filtered.csv'
		drop_indices = self.get_drop_indices(csv_file_path)
		
		final_drop_indices = np.empty(0)
		for x in drop_indices:
			i = x*5
			final_drop_indices = np.concatenate((final_drop_indices, [i,i+1,i+2,i+3,i+4]))
		final_drop_indices = final_drop_indices.astype(int)
		final_arr = np.delete(arr,final_drop_indices,axis=0)

		return final_arr

	def make_npy(self):
		'''Method to take all existing features and stream it to one binary file.
		'''
		# Create binary file to store output
		file_path = const.H_GAL_HOME_PATH+'splits/final_data.npy'
		# Check if file exists and delete it if it does
		if(os.path.exists(file_path)):
			os.remove(file_path)
		# Open file in append mode
		npy_file = open(file_path,'ab+')
		# Maintain list of file names in order
		files = []
		index = []
		ctr=0
		# Loop through all the features
		for f in glob.glob(const.H_GAL_HOME_PATH+'splits/tmp/'+'*image_features.npy'):
			temp_arr = self.get_clean_arrays(np.load(f,mmap_mode='r'),f)
			if self.verbose:
				print("Bytes:",temp_arr)
			for x in temp_arr:
				np.save(npy_file,x)
			files.append(f)
			ctr+=temp_arr.shape[0]
			index.append(ctr)
			del temp_arr
		npy_file.close()
		data_mmap = np.memmap(file_path,dtype='float32',mode='w+',shape=(ctr,2048))
		if self.verbose:
			print(data_mmap)
			print(ctr)

if __name__=='__main__':

	args = parseArgs()
	verbose, file_path = args.verbose, args.file_path

	if(verbose):
		print('\n=== ingestion.py: Start ===\n')
		print("TMP File path:",file_path)

	if file_path=='rds':
		ing_obj = Ingestion(verbose,file_path)
		ctr=0
		print('Checking file index')
		for f in glob.glob(const.H_GAL_HOME_PATH+'splits/tmp/'+'*image_features.npy'):
			temp_arr = ing_obj.get_clean_arrays(np.load(f,mmap_mode='r'),f)
			if(f==const.H_GAL_HOME_PATH+'splits/tmp/'+
				'1996-08-01_0000_US_00017469_V2_VHS52_MB19_E4_MB_image_features.npy'):
				print(ctr)
				print(ctr+temp_arr.shape[0])
			ctr+=temp_arr.shape[0]

	else:
		# Call main method
		ing_obj = Ingestion(verbose,file_path)
		ing_obj.make_npy()

	if(verbose):
		print('\n=== ingestion.py: Done ===\n')