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
import glob
import os
import sys
import warnings
import random

import pandas as pd
import numpy as np

from data import Data 

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import constants as const



from decord import VideoReader
from decord import gpu, cpu

class Model:
	"""
	This Model class is used to manage all of the classification models 
	and output of data related to the stage one of the pipeline. 
	Various methods are provided to retrieve, manipulate and store data.
	"""
	def __init__(self,file,verbose,file_path,run_on_mnt:bool):
		self.file=file
		self.verbose=verbose
		self.file_path=file_path
		if(not run_on_mnt):
			sys.path.insert(1,self.file_path+'/hxm471/inaSpeechSegmenter')
		else:
			sys.path.insert(1,const.H_PROJ_PATH+'/inaSpeechSegmenter')

		self.segmenter = __import__("segmenter")
		self.csv_path=None
		pass

	def set_csv_path(self,csv_path):
		'''Setter method.

		Args:
			csv_path (str): path to where the csv is stored.
		'''
		self.csv_path = csv_path

	def music_classification(self):
		'''Method to invoke InaSpeechSegmenter and produce segments of
		noise/music/speech intervals.
		'''
		if(self.verbose):
			print("\n-- Step 2.1.1: Initializing Segmenter --\n")
		# Initialize the segmenter
		seg = self.segmenter.Segmenter(vad_engine=const.VAD_ENGINE, detect_gender=const.DETECT_GENDER, 
				ffmpeg=const.FFMPEG_BINARY, energy_ratio=const.ENERGY_RATIO, 
				batch_size=const.BATCH_SIZE)
		if(self.verbose):
			print("\n-- Step 2.1.2: Checking output directory --\n")
		# Check output DIR
		odir = self.file_path+'/hxm471/mtvss/data/tmp/splits'
		assert os.access(odir, os.W_OK), 'Directory %s is not writable!' % odir

		with warnings.catch_warnings():
			warnings.simplefilter("ignore")

			# Extract basename of file
			base = os.path.splitext(os.path.basename(self.file))
			output_files = [os.path.join(const.SCRATCH_PATH,'tmp',base[0] + '.' + 'csv')]
			# Save CSV Path
			self.csv_path = os.path.join(const.SCRATCH_PATH,'tmp',base[0]+'.csv')

			if(self.verbose):
				print("\nbase files:\n",base[0])
				print("\nOutput files:\n",output_files)
				print("\n-- Step 2.1.3: Check if segmentation exists --\n")

			# Store start time
			start=0
			# Check for segmentation
			for f in glob.glob(const.SCRATCH_PATH+'tmp/'+base[0]+'*_loge.npy'):
				split_f = f[:-4].split('_')
				print(split_f)
				if(int(split_f[-3])==int(split_f[-2])):
					# File has been processed
					if self.verbose:
						print("File has been processed!! SKIPPING to next stage!")
					self.file_path = self.file_path+'/hxm471/video_files/'+base[0]+'.mp4'
					return
				start=split_f[-3]
			
			if self.verbose:
				print("\n-- Step 2.1.4: Starting batch process --\n")
				print("Start Time:",start)
			# Start Batch Process
			result = seg.batch_process([self.file_path+'/hxm471/video_files/'+base[0]+'.mp4'], output_files, 
				tmpdir=self.file_path,verbose=self.verbose, output_format='csv', skipifexist=False,
				start_sec=start)
			assert result[0] == 0, "Batch Process Failed!"
			self.file_path = self.file_path+'/hxm471/video_files/'+base[0]+'.mp4'
		return 

	def keyframe_extraction(self, gpu_enable:bool,file_spec:bool):
		'''This method is used to extract keyframes from music intervals.
		It uses an open-source software called Decord to efficiently seek
		and retrieve frames for specified music intervals.

		Args:
			gpu_enable (bool): Indicate if Decord should use GPU.
			file_spec (bool): Indicate if the file_path is specified.
		Returns:
			images (np.ndarray): keyframes stored as np.ndarray.
			images_batch (list): Python list containing keyframe to frame mapping.
			t_list (list): Python list containing frame to timestamp range mapping.
		'''

		if(self.verbose):
			print("\n-- Step 3.1: Initializing Decord --\n")
			print("csv_path:",self.csv_path)
			print("gpu enabled",gpu_enable)

		txt_out_path = os.path.join(const.SCRATCH_PATH+'keyframes/',
				os.path.basename(self.csv_path)[:-4]+'_keyframes.txt')
		dir_path = '/scratch/users/hxm471/keyframes/'

		if(os.path.exists(txt_out_path)):
			return

		# Get metadata
		df = pd.read_csv(self.csv_path)

		if(not file_spec):
			BASE = os.path.basename(self.csv_path)
			YEAR = BASE[0:4]
			MONTH = BASE[0:7]
			DAY = BASE[0:10]
			self.file_path = os.path.join(const.ROS_PATH,YEAR,MONTH,DAY, BASE[:-3]+'mp4')
		
		# Initialize the VideoReader
		if gpu_enable:
			vr = VideoReader(self.file_path, ctx=gpu(0))
		else:
			vr = VideoReader(self.file_path, ctx=cpu(0))
		frame_num = len(vr)

		if(self.verbose):
			print("Length of vid:",frame_num)
		
		idx=0
		# for i in range(df.index):
		# 	mtimestamp = df.iloc[i,[1,2]]
		t_list = []
		frames = []
		for i in range(0,frame_num,24):
			if(idx>=df.shape[0]):
				break

			timestamp = vr.get_frame_timestamp(i)
			mtimestamp = df.iloc[idx,[1,2]].unique()

			difftime = timestamp-mtimestamp
			if(difftime[0]>0 and difftime[1]<0):
				if(idx>len(frames)-1):
					frames.append([i,i])
					t_list.append([timestamp[0],timestamp[0]])
				elif(frames[idx][1]<i):
					frames[idx][1]=i
					t_list[idx][1]=timestamp[0]
			elif(difftime[0]<0):
				continue
			else:
				idx+=1
				continue

		images_batch = []
		images=[]
		idx=0
		for i in frames:
			images_batch.append([])
			for j in range(3):
				rand = round(random.randint(i[0],i[1]),2)
				images_batch[idx].append(rand)
			idx+=1

		# To flatten a list of lists
		images_batch_flat = [x for xs in images_batch for x in xs]
		images = vr.get_batch(images_batch_flat).asnumpy()

		d_obj = Data(None,True,self.file_path)
		d_obj.store_keyframes_txt(dir_path,txt_out_path,(images,images_batch,t_list))

		return images, images_batch, t_list