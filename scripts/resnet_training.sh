#!/bin/bash

# Load Module
module load singularity/3.8.1

cd $TMPDIR

# Copy src code
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss $TMPDIR/$USER/
# sbcast /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss /tmp/$USER/

# Copy inaSpeechSegmenter library
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter $TMPDIR/$USER/
# sbcast /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter /tmp/$USER/mtvss

# Copy image dataset
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/image_dataset $TMPDIR/$USER/

# Remove unknown class
rm -rf $TMPDIR/$USER/image_dataset/unknown

# Change directory into $USER
cd $TMPDIR/$USER/

# Make temp directory to store copies of mp4 files
mkdir $TMPDIR/$USER/video_files

# Make temp directory to store model checkpoints
mkdir $TMPDIR/$USER/model_output

# Make directory to store output
mkdir /scratch/users/$USER/jobs/interactive

# Run singularity container -- Pipeline Stage 1 -- Training Image Classifier
singularity exec -e --nv --bind /scratch/users/hxm471/,/home/hxm471/,$TMPDIR/$USER/ /scratch/users/$USER/mtvss_dev6.sif python3 $TMPDIR/$USER/mtvss/pipeline_stage1/PretrainedResNet50V2.py

# Copy model outputs to scratch
rsync -az $TMPDIR/$USER/model_output hpc3:/scratch/users/hxm471
