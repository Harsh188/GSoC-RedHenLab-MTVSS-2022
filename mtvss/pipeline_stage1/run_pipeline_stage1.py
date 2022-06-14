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

import numpy as np
import matplotlib.pyplot as plt

import time
import datetime
import argparse

from data import Data

def parseArgs():
	parser = argparse.ArgumentParser(description='Pipeline Stage 1')
	parser.add_argument('--input_dir',metavar='I',help='Path to input mp4 videos',
				default='/mnt/rds/redhen/gallina/Rosenthal/1989/1989-01/1989-01-01')
	parser.add_argument("--output_file",metavar="O",help='Path to output csv',
		default="/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/data/1989/1989-01/1989-01-01")
	parser.add_argument("--job_num",metavar="-J",help='Job number')
	parser.add_argument("--model",metavar="M",help='Music or image based classifier',default='music')
	parser.add_argument("--verbose",help='Print verbose statements to check the progress of the program',action='store_true',default=True)
	return parser.parse_args()

def main(in_path:str, out_path:str, job_num:int, verbose:bool):

	# Data
	d_obj = Data(in_path,out_path,job_num)
	files = d_obj.ingestion()

	# Model
	# m_obj = Model()

if __name__=='__main__':
	args = parseArgs()
	in_path, out_path, job_num, verbose = args.input_dir, args.output_file, args.job_num, args.verbose
	
	main(in_path, out_path, int(job_num) verbose)
