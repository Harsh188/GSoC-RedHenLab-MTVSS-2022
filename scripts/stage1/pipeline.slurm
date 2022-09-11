#!/bin/bash
#SBATCH -o /scratch/users/hxm471/jobs/arrayjob_%A_%a.o
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=20:00:00
#SBATCH --mem=30gb
#SBATCH -p gpu
#SBATCH -C gpu4v100
#SBATCH --gres=gpu:1
#SBATCH -c 2

# Load Module
module load singularity/3.8.1

cd $TMPDIR

# Copy src code
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss $TMPDIR/$USER/
# sbcast /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss /tmp/$USER/

# Copy inaSpeechSegmenter library
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter $TMPDIR/$USER/
# sbcast /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter/inaSpeechSegmenter /tmp/$USER/mtvss

# Copy model outputs
rsync -az hpc3:/scratch/users/hxm471/model_output $TMPDIR/$USER/

# Copy image dataset
rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/image_dataset $TMPDIR/$USER/

# Remove unknown class
rm -rf $TMPDIR/$USER/image_dataset/unknown

# Change directory into $USER
cd $TMPDIR/$USER/

# Make temp directory to store copies of mp4 files
mkdir $TMPDIR/$USER/video_files

# Make temp directory to store music segmentation files
mkdir $TMPDIR/$USER/seg

# Make directory to store output
mkdir /scratch/users/$USER/jobs/$SLURM_ARRAY_JOB_ID

# Move all batch output files to dir
# mv /home/$USER/*_$SLURM_ARRAY_JOB_ID_* /scratch/users/$USER/jobs/$SLURM_ARRAY_JOB_ID
mv /scratch/users/$USER/jobs/*_$SLURM_ARRAY_JOB_ID_* /scratch/users/$USER/jobs/$SLURM_ARRAY_JOB_ID

# Run singularity container -- Pipeline Stage 1 -- Music Classification
srun singularity exec -e --nv --bind /scratch/users/hxm471/,/home/hxm471/,$TMPDIR/$USER/ /scratch/users/$USER/mtvss_dev6.sif python3 $TMPDIR/$USER/mtvss/pipeline_stage1/run_pipeline_stage1.py --job_num=${SLURM_ARRAY_TASK_ID} --model="music" --verbose=True --file_path=${TMPDIR}/${USER} > /scratch/users/$USER/jobs/$SLURM_ARRAY_JOB_ID/py_output_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.txt

# Remove temporary files
rm -f -r "$TMPDIR"/*