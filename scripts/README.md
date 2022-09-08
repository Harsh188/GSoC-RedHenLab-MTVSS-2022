

To cancel all queued jobs:
```
scancel -u $USER
```

To see job status:
```
squeue -u $USER 
# or
sacct -u $USER
```

To see general info about nodes:
```
sinfo
```

Requesting GPU (example):
```
srun -p gpu -C gpu4v100 --mem=20gb --gres=gpu:1 --time=09:00:00 --pty bash 
```

Requesting CPU (example):
```
srun --nodelist=compt320 --mem=60gb -N 1 -c 40 --time=09:00:00 --pty bash 
```

```
cd gsoc

lsyncd -nodaemon -rsyncssh ./mtvss hxm471@rider.case.edu /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/mtvss
```

rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/scripts /tmp/$USER/

rsync -az gput058:/tmp/hxm471/mtvss/data/tmp/splits /mnt/rds/redhen/gallina/home/hxm471/splits

lsyncd -nodaemon -rsyncssh ./inaSpeechSegmenter hxm471@rider.case.edu /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter





rsync -e ssh -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/scripts /scratch/users/hxm471/




rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev3.sif /scratch/users/hxm471/

rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/notebooks /scratch/users/hxm471/


singularity shell --nv -e -H `pwd` --bind /scratch/users/hxm471/,/home/hxm471/,/mnt/rds/redhen/gallina/ /scratch/users/hxm471/mtvss_dev6.sif

2006-12-08_0000_US_00018523_V3_VHS16_MB13_H15_JS.mp4



srun -p gpu -C gpu4v100 --gres=gpu:1 singularity exec -e --nv --bind /scratch/users/hxm471/,/home/hxm471/,$TMPDIR/$USER/ /scratch/users/$USER/mtvss_dev5.sif python3 $TMPDIR/$USER/mtvss/pipeline_stage1/run_pipeline_stage1.py --job_num=0 --model="music" --verbose=True --file_path=${TMPDIR}

singularity exec -e --nv --bind /scratch/users/hxm471/,/home/hxm471/ /scratch/users/$USER/mtvss_dev6.sif python3 /scratch/users/hxm471/mtvss/pipeline_stage1/run_pipeline_stage1.py --job_num=0 --model="music" --verbose=True --file_path=/scratch/users/