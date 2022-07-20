

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
srun -p gpu -C gpu2v100 --mem=30gb --nodelist=gput058 --gres=gpu:1 --pty bash
```

```
cd gsoc

lsyncd -nodaemon -rsyncssh ./ hxm471@rider.case.edu /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation
```

rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/scripts /tmp/$USER/

rsync -az gput058:/tmp/hxm471/mtvss/data/tmp/splits /mnt/rds/redhen/gallina/home/hxm471/splits

lsyncd -nodaemon -rsyncssh ./inaSpeechSegmenter hxm471@rider.case.edu /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/inaSpeechSegmenter





rsync -e ssh -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/scripts /scratch/users/hxm471/




rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/Singularity/mtvss_dev3.sif /scratch/users/hxm471/

rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/notebooks /scratch/users/hxm471/


singularity shell --nv -e -H `pwd` --bind /scratch/users/hxm471/,/home/hxm471/ /scratch/users/hxm471/mtvss_dev4.sif

2006-12-08_0000_US_00018523_V3_VHS16_MB13_H15_JS.mp4