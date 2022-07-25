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
import pathlib
import os
import sys
import warnings
import random

import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import constants as const

# Deep Learning Imports
import tensorflow as tf
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet_v2 import ResNet50V2
from tensorflow.keras.applications.resnet_v2 import preprocess_input

from sklearn.metrics import classification_report

class PretrainedResNet50V2:
	'''
	'''

	def __init__(self,verbose):
		# Load and print Model
		self.model=None
		self.basemodel = ResNet50V2(include_top=False,
								weights='imagenet')
		self.basemodel.trainable = False
		print('\n--- Initialized PretrainedResNet50V2 ---\n')
		print(self.basemodel.summary())
		
		# Model Parameters
		self.IMG_SIZE = (180,180)
		self.BATCH_SIZE = 64
		self.feature_batch = None

		# Set verbose
		self.verbose=verbose


	def load_dataset(self, dataset_path):
		'''This method loads in the jpeg images for training.
		'''
		# Load dataset
		if(dataset_path!=None):
			dataset_path = const.SCRATCH_PATH+'image_dataset/'
		else:
			dataset_path = os.path.join(os.getcwd()+'/image_dataset/')
		data_dir = pathlib.Path(dataset_path)
		image_count = len(list(data_dir.glob('*/*')))
		print('Image Count:',image_count)

		# Split into train and validation set
		train_ds = tf.keras.utils.image_dataset_from_directory(
			data_dir,
			validation_split=0.2,
			subset='training',
			seed=123,
			image_size=self.IMG_SIZE,
			batch_size=self.BATCH_SIZE
		)

		val_ds = tf.keras.utils.image_dataset_from_directory(
			data_dir,
			validation_split=0.2,
			subset='validation',
			seed=123,
			image_size=self.IMG_SIZE,
			batch_size=self.BATCH_SIZE
		)

		class_names = train_ds.class_names
		print(class_names)
		for image_batch, labels_batch in train_ds:
			print(image_batch.shape)
			print(labels_batch.shape)
			break


		# Get batches
		image_batch, labels_batch = next(iter(train_ds))
		first_image = image_batch[1]
		self.feature_batch = self.basemodel(image_batch)
		print(self.feature_batch.shape)

		print(np.min(first_image), np.max(first_image))

		AUTOTUNE = tf.data.AUTOTUNE

		train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
		val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

		return train_ds,val_ds

	def train(self):
		'''
		'''

		train_ds,val_ds = self.load_dataset(None)

		num_classes = 2

		# Define Data Augmentation layer
		data_augmentation = tf.keras.Sequential([
		  tf.keras.layers.RandomFlip('horizontal'),
		  tf.keras.layers.RandomRotation(0.2),
		])

		# Define Rescaling layer
		rescale = tf.keras.layers.Rescaling(1./255)

		# Define global avg pooling
		global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
		feature_batch_average = global_average_layer(self.feature_batch)
		print(feature_batch_average.shape)

		# Define prediction layer
		prediction_layer = tf.keras.Sequential([
			tf.keras.layers.Dense(32, activation='relu'),
			tf.keras.layers.Dense(num_classes)
		])
		prediction_batch = prediction_layer(feature_batch_average)
		print(prediction_batch.shape)


		# Build model
		inputs = tf.keras.Input(shape=(180,180,3))
		x = data_augmentation(inputs)
		x = preprocess_input(x)
		x = self.basemodel(x, training=False)
		x = global_average_layer(x)
		x = tf.keras.layers.Dropout(0.2)(x)
		outputs = prediction_layer(x)

		self.model = tf.keras.Model(inputs,outputs)

		self.model.compile(
			optimizer='adam',
			loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
			metrics=['accuracy']
		)

		print(self.model.summary())

		self.model.fit(
			train_ds,
			validation_data=val_ds,
			epochs=20
		)
		pass

	def predict(self):
		pass

if __name__=='__main__':
	print('\n=== GPU Information ===\n')
	print('GPU Name:',tf.test.gpu_device_name())
	print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
	gpu=tf.config.list_physical_devices('GPU')
	if(len(gpu)):
		tf.config.experimental.set_memory_growth(gpu[0], True)

	model_obj = PretrainedResNet50V2(verbose=True)
	model_obj.train()