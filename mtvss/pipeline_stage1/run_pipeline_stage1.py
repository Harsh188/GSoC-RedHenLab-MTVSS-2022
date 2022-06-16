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
import matplotlib.pyplot as plt

import time
import datetime
import argparse

from data import Data
from model import Model

def parseArgs():
	'''Processes arugments

	Returns: parser.parse_args(): Returns populated namespace 
	'''
	parser = argparse.ArgumentParser(description='Pipeline Stage 1')
	parser.add_argument("--job_num",metavar="-J",help='Job number')
	parser.add_argument("--model",metavar="M",help='Music or image '\
		'based classifier')
	parser.add_argument("--verbose",help='Print verbose statements '\
		'to check the progress of the program')
	return parser.parse_args()

def main(job_num:int, verbose:bool):
	'''

	Args:
		job_num (int): Array Job number
		verbose (bool): If true it prints verbose statements to 
			check the progress of the program

	Returns:
		Nothing

	'''
	if(verbose):
		print("\n+++ Step 1: Data ingestion +++\n")
	
	# Data
	d_obj = Data(job_num,verbose)
	files = d_obj.ingestion()

	if(verbose):
		print("Files:",files)
		print("\n+++ Step 2: Music classification +++\n")

	# Model
	m_obj = Model(files)
	m_obj.music_classification()


if __name__=='__main__':

	args = parseArgs()
	job_num, verbose = args.job_num, args.verbose

	if(verbose):
		print('\n=== run_pipeline_stage1.py: Start ===\n')

	main(int(job_num), verbose)

	if(verbose):
		print('\n=== run_pipeline_stage1.py: Done ===\n')
