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
import tensorflow as tf

import os
from subprocess import Popen, PIPE
import multiprocessing
import threading
from threading import Thread
from queue import Queue

import code, traceback, signal
import time
import datetime
import argparse
import logging

# Functions
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
	parser.add_argument("--file_path",metavar="-F",help='tmp file path')
	return parser.parse_args()

def main(job_num:int, verbose:bool, file_path):
	'''

	'''

if __name__=='__main__':
	listen()

	args = parseArgs()
	job_num, verbose, file_path = args.job_num, args.verbose, args.file_path

	if(verbose):
		print('\n=== GPU Information ===\n')
		print('GPU Name:',tf.test.gpu_device_name())
		print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
	gpu=tf.config.list_physical_devices('GPU')
	if(len(gpu)):
		tf.config.experimental.set_memory_growth(gpu[0], True)
	if(verbose):
		print('\n=== run_pipeline_stage2.py: Start ===\n')
		print("TMP File path:",file_path)
	main(int(job_num), verbose, file_path)

	if(verbose):
		print('\n=== run_pipeline_stage2.py: Done ===\n')