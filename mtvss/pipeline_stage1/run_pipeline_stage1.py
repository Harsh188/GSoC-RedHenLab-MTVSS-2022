import numpy as np
import matplotlib.pyplt as plt

import time
import datetime
import argparse

from data import Data

def parseArgs(in_path:str, out_path:str, verbose:str):
	parser = argparse.ArgumentParser(description='Pipeline Stage 1')
	parser.add_argument('--input_dir',metavar='I',help='Path to input mp4 videos')
	parser.add_argument("--output_file",metavar="O",help='Path to output csv')
	parser.add_argument("--model",metavar="M",help='Music or image based classifier')
	parser.add_argument("--verbose",help='Print verbose statements to check \
							the progress of the program',type=bool,action='store_true')
	return parser.parse_args()

def main(in_path:str, out_path:str, verbose:bool):

	# Data
	d_obj = Data(input_dir=in_path,out_path=out_path)
	d_obj.ingestion()

	# Model

if __name__=='__main__':
	args = parseArgs()
	in_path, out_path, verbose = args.input_file, args.output_file, args.verbose
	while(True):
		try:
			main(in_path, out_path, verbose)
		except Exception as e:
			print('Exception: {}'.format(e))
