#!/bin/bash
#SBATCH -p gpu
#SBATCH -C gpu2v100
#SBATCH --gres=gpu:1
#SBATCH --mem=8gb		# Assign 8gb memory; default in 1gb
#SBATCH --output=output_%A_%a.out
#SBATCH --array=1-2

# Load Module
module load singularity/3.8.1

# Define Rosenthal folder path
rospath=/mnt/rds/redhen/gallina/Rosenthal/

# Define gallina path
galpath=/mnt/rds/redhen/gallina/

# Define singularity image path
singpath=/mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev.sif

# Process raw data first
singularity exec -e -B galpath singpath python3 /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss/data_raw.py --verbose=True

# Each array task runs the same program, but with a different input file.
n=$SLURM_ARRAY_TASK_ID
input_file=`sed -n "${n} p" input_files.txt` # Get n-th line ()

# Run singularity container -- Pipeline Stage 1 -- Music Classification
singularity exec -e -B /mnt/rds/redhen/gallina/ /mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev.sif python3 /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss/pipeline_stage1/run_pipeline_stage1.py --model='music'
