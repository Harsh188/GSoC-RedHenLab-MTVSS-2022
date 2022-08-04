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

from subprocess import Popen, PIPE

import pandas as pd
import numpy as np

from data import Data
from PretrainedResNet50V2 import PretrainedResNet50V2

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
			sys.path.insert(1,self.file_path+'/inaSpeechSegmenter')
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
		odir = '/scratch/users/hxm471/tmp'
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
					self.file_path = self.file_path+'/video_files/'+base[0]+'.mp4'
					return
				start=split_f[-3]
			
			if self.verbose:
				print("\n-- Step 2.1.4: Starting batch process --\n")
				print("Start Time:",start)
			# Start Batch Process
			result = seg.batch_process([self.file_path+'/video_files/'+base[0]+'.mp4'], output_files, 
				tmpdir=self.file_path,verbose=self.verbose, output_format='csv', skipifexist=False,
				start_sec=start)
			assert result[0] == 0, "Batch Process Failed!"
			self.file_path = self.file_path+'/video_files/'+base[0]+'.mp4'
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

	def prediction_image_extraction(self,filename,start_time,stop_time):
		'''Using start and stop times provided, extract 5 keyframe images
		for prediction.

		Args:
			filename (str): Name of file being processed
			start_time (list): list of start times for music intervals.
			stop_time (list): list of stop times for music intervals.
		Returns:
			images (np.ndarray): batches of 5 keyframe images.
		'''
		mp4_path = os.path.join(os.getcwd(),'video_files/'+filename+'.mp4')

		vr = VideoReader(mp4_path, ctx=cpu(0))
		frame_num = len(vr)

		print(start_time)

		for idx in range(len(start_time.index)):
			timestamp = (start_time.loc[idx],stop_time.loc[idx])

		idx=0
		t_list = []
		frames = []
		for i in range(0,frame_num,24):
			# Check if all music timestamps have been mapped
			if idx>=len(start_time.index):
				break
			# Get timestamp range for current frame
			timestamp = vr.get_frame_timestamp(i)
			# Get timestamp of music interval at idx
			mtimestamp = (start_time.loc[idx],stop_time.loc[idx])
			# Check if music timestamp is within frame timestamp
			difftime = timestamp-mtimestamp
			# difftime[0] > 0 - start time falls within range 
			# difftime[1] < 0 - end time falls within range
			if(difftime[0]>0 and difftime[1]<0):
				if(idx>len(frames)-1):
					frames.append([i,i])
					t_list.append([timestamp[0],timestamp[0]])
				elif(frames[idx][1]<i):
					frames[idx][1]=i
					t_list[idx][1]=timestamp[0]
			# Start time out of range
			elif(difftime[0]<0):
				continue
			# End time out of range 
			else:
				idx+=1
				continue

		if self.verbose:
			print('\n-- Keyframe Extraction --')
			print("## Length of vid:",frame_num)
			print("## Timestamps list:",t_list)
			print("## Frame mapping:",frames)
			print("## Frame mapping len:",len(frames))


		images_batch = []
		images=[]
		idx=0
		for i in frames:
			images_batch.append([])
			for j in range(5):
				rand = round(random.randint(i[0],i[1]),2)
				images_batch[idx].append(rand)
			idx+=1

		# To flatten a list of lists
		images_batch_flat = [x for xs in images_batch for x in xs]
		images = vr.get_batch(images_batch_flat).asnumpy()

		return images


	def image_filter(self):
		'''This method will use the fine-tuned ResNet50V2 to filter out any
		commercials and identify which music segements contain the title sequence.

		Args:
			
		Returns:

		'''
		# Get filename
		filename = os.path.basename(self.file)[:-4]

		# Load in pipeline progress status
		metatracker_path = os.path.join(os.getcwd(),
						'mtvss/data/tmp/metadata_tracker.csv')
		metatracker_df = pd.read_csv(metatracker_path)

		# Check if file has been processed
		idx = metatracker_df.index[metatracker_df['File_Name']==filename].tolist()[0]
		if(metatracker_df['Stage-2-Images'].loc[idx]=='Done'):
			if self.verbose:
				print('\n--- Already Filtered - SKIPPING! ---\n')
			return

		# Load the pretrained ResNet50V2 model
		model_obj = PretrainedResNet50V2(verbose=True)

		# Retrieve music segmentation timestamps
		load_path = None
		if(os.path.exists(const.SCRATCH_PATH+'tmp/'+filename+'.csv')):
			load_path = const.SCRATCH_PATH+'tmp/'+filename+'.csv'
		else:
			# Copy file from gallina to TMPDIR
			# Load rsync arguments
			csv_path = const.H_GAL_HOME_PATH+'splits/tmp/'+filename+'.csv'
			args = ["rsync","-e","ssh","-az","hpc4:"+csv_path,os.path.join(os.getcwd(),"seg")]
			# Launch rsync
			p = Popen(args, stdout=PIPE, stderr=PIPE)
			# Determine if error occured
			output,error = p.communicate()
			assert p.returncode == 0, error
			load_path = os.path.join(os.getcwd(),"seg/"+filename+'.csv')

		# Load pandas DataFrame from csv path
		seg_df = pd.read_csv(load_path)
		if self.verbose:
			print("## Segmentation CSV")
			print(seg_df.head())
			print("## Len of CSV:",len(seg_df.index))

		# Create a new DataFrame to hold classification labels
		filtered_df = pd.DataFrame(columns=['label','start','end','confidence'])

		# Get all keyframes for current file
		images = self.prediction_image_extraction(filename,seg_df['start'],seg_df['stop'])
		# Get model prediciton for all keyframe images
		output = model_obj.predict(images)
		print(output.shape)

		# Split output into batches of 5
		output = np.split(output,output.shape[0]//5)
		print(len(output))
		idx=0
		for i in output:
			print(i)
			column_avg = np.mean(i,axis=0)
			print(column_avg)
			max_class = np.argmax(column_avg,axis=0)

			if max_class==0:
				# Classification is a Commercial
				if self.verbose:
					print("## Prediction: Commercial")
					print("## Confidence:",column_avg[0])
				filtered_df.loc[len(filtered_df.index)] = ['Commercial',
															seg_df['start'].loc[idx],
															seg_df['stop'].loc[idx],
															column_avg[0]]
			else:
				# Classification is a Title Sequence
				if self.verbose:
					print("## Prediction: Title Sequence")
					print("## Confidence:",column_avg[1])
				filtered_df.loc[len(filtered_df.index)] = ['TitleSequence',
															seg_df['start'].loc[idx],
															seg_df['stop'].loc[idx],
															column_avg[1]]
			idx+=1
		# Store DataFrame
		filter_out_path = os.path.join(const.SCRATCH_PATH+'tmp/'+
										filename+'_image_filtered.csv')
		if self.verbose:
			print("## Filtered DataFrame:")
			print(filtered_df.head())
			print("## Storing dataframe:",filter_out_path)
		filtered_df.to_csv(filter_out_path)