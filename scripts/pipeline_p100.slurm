#!/bin/bash
#SBATCH -N 1
#SBATCH -p gpu
#SBATCH -C gpup100
#SBATCH --gres=gpu:1
#SBATCH --mem=30gb              # Assign 16gb memory; default in 1gb
#SBATCH -c 2
#SBATCH -o /scratch/users/hxm471/jobs/arrayjob_%A_%a.o
#SBATCH --time=09:00:00
#SBATCH -n 1

# Load Module
module load singularity/3.8.1

cd $TMPDIR

# Copy src code
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss $TMPDIR/$USER/
# sbcast /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss /tmp/$USER/

# Copy inaSpeechSegmenter library
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter $TMPDIR/$$
# sbcast /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter /tmp/$USER/mtvss

# Change directory into $USER
cd $TMPDIR/$USER/

# Make temp directory to store copies of mp4 files
mkdir $TMPDIR/$USER/video_files

# Make directory to store output
mkdir /scratch/users/$USER/jobs/$SLURM_ARRAY_JOB_ID

# Move all batch output files to dir
mv /scratch/users/$USER/jobs/*_$SLURM_ARRAY_JOB_ID_* /scratch/users/$USER/jobs/$SLURM_ARRAY_JOB_ID

# Run singularity container -- Pipeline Stage 1 -- Music Classification
srun singularity exec -e --nv --bind /scratch/users/hxm471/,/home/hxm471/,$TMPDIR/$USER/ /scratch/users/$USER/mtvss_dev6.sif python3 $TMPDIR$

# Transfer features & CSVs
rsync -az $TMPDIR/$USER/mtvss/data/tmp/splits hpc3:/mnt/rds/redhen/gallina/home/hxm471/

# Remove temporary files
rm -f -r "$TMPDIR"/*

