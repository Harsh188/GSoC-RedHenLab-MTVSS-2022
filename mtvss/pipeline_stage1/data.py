import os
import glob

class Data:


	def __init__(self, input_dir:str, output_dir:str):
		self.input_dir = input_dir
		self.output_dir = output_dir

	def ingestion(self):
		if(not os.path.isdir(self.input_dir)):
			raise Exception("Error! Input directory does not exist:",input_dir)
		mp4_files = glob.iglob(input_dir+"**/.mp4",recursive=True)
		for file in files:
			pass

	def eda(self):
		pass


	def preprocess(self):
		pass
