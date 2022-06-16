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
alias rospath=/mnt/rds/redhen/gallina/Rosenthal/

# Define gallina path
alias galpath=/mnt/rds/redhen/gallina/

# Define singularity image path
alias singpath=/mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev.sif

# Process raw data first
singularity exec -e -B /mnt/rds/redhen/gallina/ /mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev.sif python3 /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss/data_raw.py --verbose=True