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
import numpy as np

from sklearn.neighbors import KNeighborsTransformer

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import constants as const

class Model:
	'''
	'''

	def __init__(self,verbose,file_path,run_on_mnt):
		'''

		'''
		self.verbose=verbose
		self.file_path=file_path

		if(not run_on_mnt):
			sys.path.insert(1,self.file_path+'/sklearn_ann/cluster')
		else:
			sys.path.insert(1,const.H_PROJ_PATH+'sklearn_ann/cluster')

		self.RnnDBSCAN = __import__('rnn_dbscan')

	def run_rnn_dbscan(self,data):
		'''
		'''
		n_neighbors = 2
		pipeline = self.RnnDBSCAN.simple_rnn_dbscan_pipeline(KNeighborsTransformer, n_neighbors)
		labels = pipeline.fit_predict(data)
		db = pipeline.named_steps["rnndbscan"]
		core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
		core_samples_mask[db.core_sample_indices_] = True

		# Number of clusters in labels, ignoring noise if present.
		n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
		n_noise_ = list(labels).count(-1)

		if self.verbose:
			print('Estimated number of clusters: %d' % n_clusters_)
			print('Estimated number of noise points: %d' % n_noise_)
			print("Homogeneity: %0.3f" % metrics.homogeneity_score(y, labels))
			print("Completeness: %0.3f" % metrics.completeness_score(y, labels))
			print("V-measure: %0.3f" % metrics.v_measure_score(y, labels))
			print("Adjusted Rand Index: %0.3f"
			      % metrics.adjusted_rand_score(y, labels))
			print("Adjusted Mutual Information: %0.3f"
			      % metrics.adjusted_mutual_info_score(y, labels))
			print("Silhouette Coefficient: %0.3f"
			      % metrics.silhouette_score(data, labels))