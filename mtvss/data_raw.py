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
import argparse

import pandas as pd

def parseArgs():
	parser = argparse.ArgumentParser(description='Process raw data')
	parser.add_argument('--input_dir',metavar='-I',help='Path to Rosenthal dir',
				default='/mnt/rds/redhen/gallina/Rosenthal/')
	parser.add_argument("--output_file",metavar="-O",help='Path to output dir',
		default="/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/data/temp/")
	return parser.parse_args()

def create_batches(input_dir):
	input_file = '/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/data/temp/raw_cat1.csv'
	store_file = '/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/data/temp/batch_cat1.csv'
	if(os.path.isfile(store_file)):
		return
	BATCH_SIZE=100
	batches = []
	if(os.path.isfile(input_file)):
		df = pd.read_csv(input_file)
		for g, df_sub in df.groupby(np.arange(len(df)) // BATCH_SIZE):
		    print()
		    batches.append(df_sub['File Path'].values[:])
			batches_df = pd.DataFrame(result)
			batches_df.to_csv()
	else:
		pass


if __name__=='__main__':
	args = parseArgs()
	input_dir = args.input_dir
	create_batches(input_dir)