#!/bin/bash
#SBATCH -p gpu
#SBATCH -C gpu2v100
#SBATCH --gres=gpu:1
#SBATCH --mem=8gb		# Assign 8gb memory; default in 1gb
#SBATCH --array=0-26

# Load Module
module load singularity/3.8.1

# Define Rosenthal folder path
rospath=/mnt/rds/redhen/gallina/Rosenthal/

# Define gallina path
galpath=/mnt/rds/redhen/gallina/

# Define singularity image path
singpath=/mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev.sif

# Copy src code
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss /tmp/$USER/
# Copy inaSpeechSegmenter library
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter /tmp/$USER/mtvss
# Copy singularity image
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev.sif /tmp/$USER/

# Change directory into $USER
cd /tmp/$USER/

# Make temp directory to store copies of mp4 files
mkdir /tmp/$USER/mtvss/data/tmp/video_files

# TODO:
# Write script to read batch of Rosenthal files based on Array Job Index
n=$SLURM_ARRAY_TASK_ID
i=0
allFiles=()
while IFS= read -r line; do
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
singularity exec -e --nv -B /tmp/$USER/ /tmp/$USER/mtvss_dev.sif python3 /tmp/$USER/mtvss/pipeline_stage1/run_pipeline_stage1.py --job_num=${SLURM_ARRAY_TASK_ID} --model="music" --verbose=True

# Remove temporary files
rm -f -r /tmp/$USER/