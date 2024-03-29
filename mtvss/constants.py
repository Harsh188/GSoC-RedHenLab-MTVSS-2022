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

# Rosenthal directory path
ROS_PATH='/mnt/rds/redhen/gallina/Rosenthal/'

# Scratch directory path
SCRATCH_PATH='/scratch/users/hxm471/'

# Harshith's gallina home directory path
H_GAL_HOME_PATH = '/mnt/rds/redhen/gallina/home/hxm471/'

# Harshith's gallina project directory path
H_PROJ_PATH= H_GAL_HOME_PATH+'RedHenLab-Multimodal_TV_Show_Segmentation/'

# Temporary data storage path
TMP_PATH=H_PROJ_PATH+'mtvss/data/tmp/'

# Temporary batch storage path
TMP_BATCH_PATH=TMP_PATH+'batch_cat1.npy'

## DATA Related Constants

# mp4 file processing batch size
MP4_FILE_BATCH_SIZE=100

# Starting index of the file name (used to remove path info)
FILE_START_INDEX=58
# Starting index of the folder
FOLDER_START_INDEX=33

# Constant label values which are extracted from the file name
COLUMN_LABELS=['Pull Date','Year','Month','Day','TODO','Lang','Barcode','V No.','File Type','File Path']

## InaSpeechSegmenter Constants

BATCH_SIZE=1024
VAD_ENGINE='smn'
DETECT_GENDER=False
FFMPEG_BINARY='ffmpeg'
EXPORT_FORMAT='csv'
ENERGY_RATIO=0.03