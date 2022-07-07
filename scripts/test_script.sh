#!/bin/bash

# Makes the bash script to print out every command before it is executed except echo
# trap '[[ $BASH_COMMAND != echo* ]] && echo $BASH_COMMAND' DEBUG

# Load Module
module load singularity/3.8.1

# Copy src code
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss /tmp/$USER/
# sbcast /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss /tmp/$USER/

# Copy inaSpeechSegmenter library
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter /tmp/$USER/
# sbcast /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter /tmp/$USER/mtvss

# Change directory into $USER
cd /tmp/$USER/

# Make temp directory to store copies of mp4 files
mkdir /tmp/$USER/video_files

# Write script to read batch of Rosenthal files based on Array Job Index 0
# n=0
# i=0
# allFiles=()
# while IFS= read -r line; do
# 	if [ $i -eq $n ] 
# 	then
# 		echo i equal to n
# 		allFiles+=($line)
		
# 		for f in ${allFiles[@]}; do
# 			echo $f
# 			rsync -az hpc3:${f} /tmp/$USER/video_files
# 		done
# 	fi
# 	i=$((i+1))
# done < /tmp/$USER/mtvss/data/tmp/batch_cat1.txt

# Run singularity container -- Pipeline Stage 1 -- Music Classification
singularity exec -e --nv -B /tmp/$USER/ /scratch/users/$USER/mtvss_dev4.sif python3 -m memray run /tmp/$USER/mtvss/pipeline_stage1/run_pipeline_stage1.py --job_num=0 --model="music" --verbose=True

# Remove temporary files
# rm -f -r /tmp/$USER/