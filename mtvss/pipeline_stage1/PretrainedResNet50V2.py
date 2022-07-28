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
import matplotlib.pyplot as plt

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
		self.IMG_SIZE = (400,400)
		self.BATCH_SIZE = 64
		self.feature_batch = None

		# Set verbose
		self.verbose=verbose

	def build_model(self):
		'''Method to build the model.
		'''
		# Define number of classes
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
			tf.keras.layers.Dense(num_classes, activation='softmax')
		])
		prediction_batch = prediction_layer(feature_batch_average)
		print(prediction_batch.shape)

		# Build model
		inputs = tf.keras.Input(shape=(400,400,3))
		x = data_augmentation(inputs)
		x = preprocess_input(x)
		x = self.basemodel(x, training=False)
		x = global_average_layer(x)
		x = tf.keras.layers.Dropout(0.2)(x)
		outputs = prediction_layer(x)

		# Set model
		self.model = tf.keras.Model(inputs,outputs)
		print("Model:",self.model)

	def load_dataset(self, dataset_path):
		'''This method loads in the jpeg images for training.

		Args:
			dataset_path (str): Path to load in the data for training.

		Returns:
			train_ds (): Train dataset split
			val_ds (): Validation dataset split
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
			label_mode='categorical',
			validation_split=0.2,
			subset='training',
			seed=123,
			image_size=self.IMG_SIZE,
			batch_size=self.BATCH_SIZE
		)

		val_ds = tf.keras.utils.image_dataset_from_directory(
			data_dir,
			label_mode='categorical',
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

		print(list(val_ds))

		return train_ds,val_ds

	def save_plots(self, history, out_path):
		'''Method to create epoch vs accuracy and epoch vs loss plots
		and saves them.

		Args:
			history (History): History object from tensorflow.
			out_path (str): Path to store the figures.
		'''

		# Load in all the values from history
		training_loss = history.history['loss']
		test_loss = history.history['val_loss']
		training_acc = history.history['accuracy']
		test_acc = history.history['val_accuracy']
		
		# Get the epoch count
		epoch_count = [i for i in range(1,history.params['epochs']+1)]
		
		if self.verbose:
			print("\n### Saving Model Plots")
			print("#### Training_loss:",training_loss)
			print("#### Test_loss:",test_loss)
			print("#### Training_acc:",training_acc)
			print("#### Test_acc:",test_acc)
			print("#### Epoch_count:",epoch_count)
			print("#### Output dir:",out_path)

		# Visualize loss history
		plt.plot(epoch_count, training_loss, 'r--')
		plt.plot(epoch_count, test_loss, 'b-')
		plt.legend(['Training Loss', 'Test Loss'])
		plt.xlabel('Epoch')
		plt.ylabel('Loss')
		plt.title("Epoch vs Loss")
		plt.savefig(out_path+'_LossPlots.svg');

		plt.clf()

		# Visualize accuracy history
		plt.plot(epoch_count, training_acc, 'r--')
		plt.plot(epoch_count, test_acc, 'b-')
		plt.legend(['Training Accuracy', 'Test Accuracy'])
		plt.xlabel('Epoch')
		plt.ylabel('Accuracy')
		plt.title("Epoch vs Accuracy")
		plt.savefig(out_path+'_AccuracyPlots.svg');

	def train(self):
		'''Builds and trains the model. Then it saves the weights
		and plots.
		'''

		# Get train and validation splits
		train_ds,val_ds = self.load_dataset(None)

		# Build the model
		self.build_model()

		# Compile the model
		self.model.compile(
			optimizer='adam',
			loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
			metrics=['accuracy']
		)

		# Print the model summary
		print(self.model.summary())

		# Start training
		history = self.model.fit(
			train_ds,
			validation_data=val_ds,
			epochs=40
		)
		
		# Save the model
		print(os.path.join(os.getcwd(),'model_output'))
		if (not os.path.exists(os.path.join(os.getcwd(),'model_output'))):
			os.mkdir(os.path.join(os.getcwd(),'model_output'))
		checkpoint_dir = os.path.join(os.getcwd(),'model_output/pretrainedResNet50V2')

		# Save the weights
		self.model.save_weights(checkpoint_dir)

		# Save plots
		self.save_plots(history,checkpoint_dir)


	def predict(self,data):
		'''This method is used to predict the output on the
		data given.

		Args:
			data (np.ndarray): Image to get classification output.
		'''
		# Set feature batch
		self.feature_batch = self.basemodel(data)

		# Build the model
		self.build_model()
		# Get checkpoints dir
		checkpoint_dir = os.path.join(os.getcwd(),'model_output/pretrainedResNet50V2')
		# Load weights into model
		self.model.load_weights(checkpoint_dir)
		print(self.model)

		# Load images
		imgs = tf.image.resize(data,size=self.IMG_SIZE)

		# Make prediction
		prediction = self.model.predict(imgs)
		print("prediction:",prediction)
		return prediction

if __name__=='__main__':
	print('\n=== GPU Information ===\n')
	print('GPU Name:',tf.test.gpu_device_name())
	print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
	gpu=tf.config.list_physical_devices('GPU')
	if(len(gpu)):
		tf.config.experimental.set_memory_growth(gpu[0], True)

	model_obj = PretrainedResNet50V2(verbose=True)
	model_obj.train()
	# model_obj.predict()