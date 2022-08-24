#!/bin/bash

# Load Module
module load singularity/3.8.1

cd $TMPDIR

# Copy src code
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss $TMPDIR/$USER/

# Copy sklearn-ann library
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/sklearn-ann/sklearn_ann $TMPDIR/$USER/

# Change directory into $USER
cd $TMPDIR/$USER/

# Run singularity container -- Pipeline Stage 1 -- Music Classification
singularity exec -e --nv --bind /scratch/users/hxm471/,/home/hxm471/,$TMPDIR/$USER/ /scratch/users/$USER/mtvss_dev6.sif python3 $TMPDIR/$USER/mtvss/pipeline_stage2/run_pipeline_stage2.py --verbose=True --file_path=${TMPDIR}/${USER} --mode='opt'

# Remove temporary files
# rm -f -r /tmp/$USER/