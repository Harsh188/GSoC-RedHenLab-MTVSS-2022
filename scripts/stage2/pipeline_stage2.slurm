#!/bin/bash
#SBATCH -o /scratch/users/hxm471/jobs/arrayjob_%A.o
#SBATCH -N 1
#SBATCH --time=12:00:00
#SBATCH --mem=60gb
#SBATCH --nodelist compt317

# Load Module
module load singularity/3.8.1

cd $TMPDIR

# Copy src code
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss $TMPDIR/$USER/

# Copy sklearn-ann library
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/sklearn-ann/sklearn_ann $TMPDIR/$USER/

# Change directory into $USER
cd $TMPDIR/$USER/

# Make directory to store output
mkdir /scratch/users/$USER/jobs/$SLURM_JOB_ID

# Move all batch output files to dir
mv /scratch/users/$USER/jobs/*_$SLURM_JOB_ID* /scratch/users/$USER/jobs/$SLURM_JOB_ID

# Run singularity container -- Pipeline Stage 1 -- Music Classification
singularity exec -e --nv -H `pwd` --bind /scratch/users/hxm471/,/home/hxm471/,/mnt/rds/redhen/gallina/,$TMPDIR/$USER/ /scratch/users/$USER/mtvss_dev6.sif python3 $TMPDIR/$USER/mtvss/pipeline_stage2/run_pipeline_stage2.py --verbose=True --file_path=${TMPDIR}/${USER} --mode='opt' > /scratch/users/$USER/jobs/$SLURM_JOB_ID/py_output_${SLURM_JOB_ID}.txt

# Remove temporary files
rm -f -r "$TMPDIR"/*