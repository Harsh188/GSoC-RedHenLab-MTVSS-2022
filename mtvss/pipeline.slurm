#!/bin/bash
#SBATCH -p gpu
#SBATCH -C gpu4v100
#SBATCH --gres=gpu:1
#SBATCH -mem=8gb		# Assign 8gb memory; default in 1gb
#SBATCH --output=output_%A_%a.out
#SBATCH --array=1-2

# Load Module
module load singularity

# Each array task runs the same program, but with a different input file.
n=$SLURM_ARRAY_TASK_ID
input_file=`sed -n "${n} p" input_files.txt` # Get n-th line ()

# Run singularity container
singularity exec -e -B /mnt/rds/redhen/gallina/ cd /mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev.sif 