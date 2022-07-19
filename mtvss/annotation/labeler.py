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
import sys

import pandas as pd
import numpy as np
import cv2

class Labeler:

	def __init__(self,keyframes_path:str,output_path:str):
		self.keyframes_path = keyframes_path
		if(os.path.exists(output_path)==False):
			try:
				os.makedirs(output_path)
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise
		assert os.path.exists(output_path)==True
		self.output_path = output_path

	def launch_annotator(self):
		for f in glob.glob(os.path.join(self.keyframes_path,'*.npy')):
				print(f)