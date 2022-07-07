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

import time
import datetime
import argparse
import logging

from data import Data
from model import Model

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
	return parser.parse_args()

def display(msg):
	threadname = threading.current_thread().name
	processname = multiprocessing.current_process().name
	print(f'{processname}\\{threadname}: {msg}')

# Producer
def load_files(files,loaded_files,finished,verbose):
	'''Method to load the mp4 files using multi-threading. This method
	acts as the producer.

	Args:
		files (np.ndarray): MP4 file path in gallina
		loaded_files (Queue):
		finished (Queue):
	
	Returns:
	'''
	# Finished Queue to indicate status of producer
	finished.put(False)
	# Counter variable
	ctr=0
	# Loop through all the files in the batch
	for f in files:
		if (verbose):
			display(f'Producing {ctr}: {f}')

		# Load rsync arguments
		args = ["rsync","-e","ssh","-az","hpc4:"+str(f),"/tmp/hxm471/video_files"]
		# Launch rsync
		p = Popen(args, stdout=PIPE, stderr=PIPE)
		# Determine if error occured
		output,error = p.communicate()
		assert p.returncode == 0, error
		# Add rsynced file to Queue
		loaded_files.put(f)
		ctr+=1

	# Indicate producer is done
	finished.put(True)
	if(verbose):
		display('finished')

# Consumer
def process_files(loaded_files,finished,verbose):
	'''Method to take loaded files and process them using multi-threading.
	This method acts as the consumer.

	Args:
		loaded_files (Queue):
		finished (Queue):
	Returns:
	'''

	# Counter variable
	ctr=0
	while True:
		if not loaded_files.empty():
			# Get the loaded file
			f = loaded_files.get()
			if(verbose):
				display(f'Consuming {ctr}: {f}')

			# Perform Music Classification
			if verbose:
				print('\n-- Step 2.1 Music Classification --\n')
			m_obj = Model(f,verbose)
			m_obj.music_classification()

			if verbose:
				print('\n-- Step 2.2 Remove mp4 File --\n')
			# Extract basename of file
			base = os.path.splitext(os.path.basename(f))
			# Load rm arguments
			args = ["rm","-rf","/tmp/hxm471/video_files/"+base[0]]
			# Launch rm
			p = Popen(args, stdout=PIPE, stderr=PIPE)
			# Determine if error occured
			output,error = p.communicate()
			assert p.returncode == 0, error

			# Increment counter
			ctr+=1
		else:
			if verbose:
				display(f'Consumer {ctr}:Q empty')
			# Exit loop if producer is done
			status = finished.get()
			if status == True:
				break
			else:
				finished.put(False)
			time.sleep(10)
	if(verbose):
		display('finished')

def main(job_num:int, verbose:bool):
	'''This method runs the music classification and title sequence
	image based filtering. This completes the first stage of the pipeline.
	The output is a noisy metadata consisting of:
		1. Filename		(str)
		2. Category number	(int)
		3. Start times	(array)
		5. Stop times	(array)
		6. Audio features	(str)
		7. Title sequence images (array)

	Args:
		job_num (int): Array Job number
		verbose (bool): If true it prints verbose statements to 
			check the progress of the program

	Returns:
		TODO

	'''
	if(verbose):
		print("\n+++ Step 1: Data ingestion +++\n")
	
	# Data
	d_obj = Data(job_num,verbose)
	files = d_obj.ingestion()
	
	if verbose:
		print(files)

	# Create a queue to hold loaded files
	loaded_files = Queue(maxsize=8)
	finished = Queue()

	if verbose:
		print('\n+++ Step 2: Multi-threaded Consumer-Producer +++')
	producer = Thread(target=load_files, args=[files,loaded_files,finished,verbose]
						,daemon=True)
	consumer = Thread(target=process_files, args=[loaded_files,finished,verbose]
						,daemon=True)

	producer.start()
	consumer.start()

	producer.join()
	if(verbose):
		display('Producer has finished\n')

	consumer.join()
	if verbose:
		display('Consumer has finished\n')


if __name__=='__main__':

	args = parseArgs()
	job_num, verbose = args.job_num, args.verbose

	if(verbose):
		print('\n=== GPU Information ===\n')
		print('GPU Name:',tf.test.gpu_device_name())
		print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
	gpu=tf.config.list_physical_devices('GPU')
	if(len(gpu)):
		tf.config.experimental.set_memory_growth(gpu[0], True)
	if(verbose):
		print('\n=== run_pipeline_stage1.py: Start ===\n')

	main(int(job_num), verbose)

	if(verbose):
		print('\n=== run_pipeline_stage1.py: Done ===\n')
