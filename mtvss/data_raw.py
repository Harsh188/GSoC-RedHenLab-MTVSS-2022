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
import argparse

import pandas as pd
import numpy as np
import glob

import constants as const

def parseArgs():
	'''Processes arugments

	Returns: parser.parse_args(): Returns populated namespace 
	'''
	parser = argparse.ArgumentParser(description='Process raw data')
	parser.add_argument('--verbose',help='Print verbose statements'\
		'to check the progress of the program',default=False)
	return parser.parse_args()

def traverse_iglob(files,verbose):
	'''Method to traverse through all of the iglob files recursively

	Args:
		files (iglob):

	Returns:
		ctr (int):
		files_split (List):
	'''

	# Establish a counter variable to keep track of no of files.
	ctr=0
	# Maintain a list to extract only the file names
	files_split=[]

	# Loop through the iglob iterator and update the variables
	for file in files:
		if(verbose):
			print(file)
		ctr+=1
		file_split = file[const.FILE_START_INDEX:].split('_')
		year, month, day = file_split[0].split('-')
		files_split.append([file_split[0]]+[year]+[month]+[day]
			+file_split[1:5]+[file_split[-1]]+[file[const.FILE_START_INDEX:]])
	if(verbose):
		print('\n\n\n+++ Done reading mp4 files +++\n\n\n')
	return ctr,files_split

def create_raw(verbose):
	'''
	'''
	INPUT_PATH = const.ROS_PATH
	OUTPUT_PATH = const.TMP_PATH+'raw_cat1.csv'

	# Check if output file already exists
	if(os.path.isfile(OUTPUT_PATH)):
		if(verbose):
			print('\n+++ Raw Output Exists: Exiting +++\n')
		# If it does then just exit
		return
	# Check if Rosenthal folder exists
	if(os.path.isdir(INPUT_PATH)):
		print('\n+++ Raw Output does not exist: Starting Process +++\n')
		
		# Crete iglob iterator for all mp4 files
		mp4_files = glob.iglob(INPUT_PATH+"**/*.mp4", recursive=True)

		# Use method to extract file count and name
		mp4_ctr, mp4_files_split = traverse_iglob(mp4_files,verbose)

		# Create pandas DataFrame for all mp4 files
		mp4_df = pd.DataFrame(mp4_files_split, columns=const.COLUMN_LABELS)

		# Basic filter
		# Remove V No. with frequency less than 10
		THRESHOLD = 100
		value_counts = mp4_df['V No.'].value_counts()
		to_remove = value_counts[value_counts <= THRESHOLD].index
		mp4_filtered_df = mp4_df.replace(to_remove, np.nan, inplace=False)
		mp4_filtered_df.dropna()

		cat1_df = mp4_filtered_df.loc[(mp4_filtered_df['V No.']=='V1')|(mp4_filtered_df['V No.']=='V2')|(mp4_filtered_df['V No.']=='V3')]
		cat1_df = cat1_df.loc[cat1_df['Year'].astype(int)>=1995]
		cat1_df.to_csv(OUTPUT_PATH)
	return

def create_batches(verbose):
	'''
	'''
	INPUT_PATH = const.TMP_PATH+'raw_cat1.csv'
	OUTPUT_PATH = const.TMP_BATCH_PATH

	# Check if output file already exists
	if(os.path.isfile(OUTPUT_PATH)):
		print('\n+++ Batches Output Exists: Exiting +++\n')
		# If it does then just exit
		return
	# If not create batches
	batches = []
	# Check if raw csv file exists
	if(os.path.isfile(INPUT_PATH)):
		print('\n+++ Batch Output does not exist: Starting Process +++\n')
		df = pd.read_csv(INPUT_PATH)
		for g, df_sub in df.groupby(np.arange(len(df)) // const.MP4_FILE_BATCH_SIZE):
		    batches.append(df_sub['File Path'].values[:])
		batches=np.array(batches)
		np.save(OUTPUT_PATH)
	else:
		pass

if __name__=='__main__':
	global verbose
	args = parseArgs()
	verbose = args.verbose
	if(verbose):
		print('\n=== data_raw.py: Start ===\n')
	create_raw(verbose)
	create_batches(verbose)
	if(verbose):
		print('\n=== data_raw.py: Done ===\n')
