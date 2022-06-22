#!/bin/bash

# Makes the bash script to print out every command before it is executed except echo
# trap '[[ $BASH_COMMAND != echo* ]] && echo $BASH_COMMAND' DEBUG

# Copy src code
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss /tmp/$USER/
# Copy inaSpeechSegmenter library
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter /tmp/$USER/mtvss
# Copy singularity image
<<<<<<< HEAD
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev2.sif /tmp/$USER/

# Copy singularity cache
rsync -az hpc3:/home/hxm471/.singularity
=======
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev.sif /tmp/$USER/
>>>>>>> 5bc8799d624305fd5d322fe6c0a19e3097d4ebad

# Change directory into $USER
cd /tmp/$USER/

# Make temp directory to store copies of mp4 files
mkdir /tmp/$USER/mtvss/data/tmp/video_files

<<<<<<< HEAD
# Create symbolic link to .singularity
ln -s /home/hxm471/.singularity /mnt/rds/redhen/gallina/home/hxm471/.singularity

=======
>>>>>>> 5bc8799d624305fd5d322fe6c0a19e3097d4ebad
# Load Module
module load singularity/3.8.1

# TODO:
# Write script to read batch of Rosenthal files based on Array Job Index
n=26
i=0
allFiles=()
while IFS= read -r line; do
	echo $i
	if [ $i -eq $n ] 
	then
		echo i equal to n
		allFiles+=($line)
		
		for f in ${allFiles[@]}; do
			echo $f
			rsync -az hpc3:${f} /tmp/$USER/mtvss/data/tmp/video_files
		done
	fi
	i=$((i+1))
done < /tmp/$USER/mtvss/data/tmp/batch_cat1.txt

# Run singularity container -- Pipeline Stage 1 -- Music Classification
<<<<<<< HEAD
singularity exec -e --nv -B /tmp/$USER/ /tmp/$USER/mtvss_dev2.sif python3 /tmp/$USER/mtvss/pipeline_stage1/run_pipeline_stage1.py --job_num=$n --model="music" --verbose=True
=======
singularity exec -e --nv -B /tmp/$USER/ /tmp/$USER/mtvss_dev.sif python3 /tmp/$USER/mtvss/pipeline_stage1/run_pipeline_stage1.py --job_num=$n --model="music" --verbose=True
>>>>>>> 5bc8799d624305fd5d322fe6c0a19e3097d4ebad

# Remove temporary files
# rm -f -r /tmp/$USER/