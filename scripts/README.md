

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
srun -p gpu -C gpu2v100 --mem=9gb --gres=gpu:1 --nodelist=gput059 --pty bash
```

```
cd gsoc

lsyncd -nodaemon -rsyncssh ./ hxm471@rider.case.edu /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation
```

rsync -az hpc3:/mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation/scripts /tmp/$USER/
