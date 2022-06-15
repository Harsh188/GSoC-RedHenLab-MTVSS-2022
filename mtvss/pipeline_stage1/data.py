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

class Data:
	"""
	This Data class is used to manage all of the ingestion and output of data related to the stage one of the pipeline. Various methods are provided to retrieve, manipulate and store data.
	"""

	def __init__(self, input_dir:str, output_dir:str,job_num:int):
		self.input_dir = input_dir
		self.output_dir = output_dir
		self.job_num = job_num

	def ingestion(self) -> np.ndarray:
		"""The ingestion method is used to pull in all the mp4 files related to a certain category. The files are stored in batches and based on the Array job number, the corresponding batch is returned.
		
		Args:
			category (str): TODO
		Returns:
			batches (List): List of mp4 files.
		"""
		batch_path = '/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/data/tmp/batch_cat1.npy'
		if(not os.path.isfile(batch_path)):
			raise Exception("Batch file does not exist!")
		else:
			batches = np.load(batch_path, allow_pickle=True)
			print(batches[self.job_num])
			return batches[self.job_num]

	def eda(self):
		pass


	def preprocess(self):
		pass
