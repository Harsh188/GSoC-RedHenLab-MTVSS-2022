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

import os

import code, traceback, signal
import time
import datetime
import argparse
import logging

from data import Data
from model import Model

import cProfile

# Functions
def parseArgs():
	'''Processes arugments

	Returns: parser.parse_args(): Returns populated namespace 
	'''
	parser = argparse.ArgumentParser(description='Pipeline Stage 2')
	parser.add_argument("--verbose",help='Print verbose statements '\
		'to check the progress of the program')
	parser.add_argument("--file_path",metavar="-F",help='tmp file path')
	parser.add_argument("--mode",metavar="-M",help='Which mode to run the pipeline')
	return parser.parse_args()

def main(verbose:bool, file_path, mode:str):
	'''This method runs RNN-DBSCAN on image features extraced from the 
	stage one of the pipeline. Stage two results in clustered features.

	Args:
		verbose (bool): If true it prints verbose statements to 
			check the progress of the program
		file_path (str): Path of current directory
		mode (str): The mode in which the pipeline should be run: {opt,final}
			Where 'opt' indicates optimization mode to perform analysis on
			a subset of the data and 'final' indicates the production ready code.
	Returns:
		Nothing
	'''
	if(verbose):
		print("\n\n+++ Step 1: Data ingestion +++\n\n")

	# Data
	d_obj = Data(verbose,file_path)
	data = None
	if mode=='final':
		data = d_obj.ingestion()
	elif mode=='opt':
		data = d_obj.optimization_ingestion()
	
	if(verbose):
		print("## Ingested data:")
		print(data[0])

	# Clustering
	m_obj = Model(verbose,file_path,run_on_mnt=False)
	m_obj.run_rnn_dbscan(data)


if __name__=='__main__':

	args = parseArgs()
	verbose, file_path, mode = args.verbose, args.file_path, args.mode

	if(verbose):
		print('\n=== run_pipeline_stage2.py: Start ===\n')
		print("TMP File path:",file_path)
	
	# Call main method
	if mode=='test':
		cProfile.run('main(verbose,file_path,mode)')
	else:
		main(verbose,file_path,mode)
	if(verbose):
		print('\n=== run_pipeline_stage2.py: Done ===\n')