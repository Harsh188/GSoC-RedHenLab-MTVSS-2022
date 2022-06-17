# RedHenLab-Multimodal_TV_Show_Segmentation

This proposal proposes a multi-modal multi-phase pipeline to tackle television show segmentation on the Rosenthal videotape collection. The two-stage pipeline will begin with feature filtering using pre-trained classifiers and heuristic-based approaches. This stage will produce noisy title sequence segmented data containing audio, video, and possibly text. These extracted multimedia snippets will then be passed to the second pipeline stage. In the second stage, the extracted features from the multimedia snippets will be clustered using RNN-DBSCAN. Title sequence detection is possibly the most efficient path to high precision segmentation for the first and second tiers of the Rosenthal collection (which have fairly structured recordings). This detection algorithm may not bode well for the more unstructured V8+ and V4 VCR tapes in the Rosenthal collection. Therefore the goal is to produce accurate video cuts and split metadata results for the first and second tiers of the Rosenthal collection.


## Usage

### Local Development

#### Singularity 

TODO:

#### Docker Container

1. To build the docker image run the following command

```
docker-compose up
```

This command builds the docker image which can then be used to start up the container.

2. Next use the following command to start up the docker container

```
docker run --gpus all -it --rm -p 8888:8888 -v $PWD:/MultiModalTVShowSeg-2022 redhenlab-multimodal_tv_show_segmentation_dev
```

#### Jupyter Notebook

Once the container is up and running use the following code to launch jupyter notebooks.

```
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

### Remote Development

The following set of instructions are to be used when developing on the CWRU HPC.

#### Singularity
1. Start a screen session
```
screen -S singularity
```

or reattach to existing screen

```
screen -r
```

2. Navigate to dir on HPC
```
cd /mnt/rds/redhen/gallina/home/hxm471/RedHenLab-Multimodal_TV_Show_Segmentation
```

3. Start singularity shell
```
module load singularity/3.8.1
singularity shell -e -H `pwd` -B /mnt/rds/redhen/gallina/ ./singularity/mtvss_dev.sif
```

#### Jupyter Notebook

Once inside the singularity container, use the following commands to launch the jupyter notebook.

1. Run the jupyter-notebook within existing singularity shell
```
jupyter notebook --ip 127.0.0.1 --port 8889 --no-browser
```

2. Establish ssh port forwarding to acess jupyter notebook on local machine
```
ssh -N -f -L localhost:8889:localhost:8889 hxm471@rider.case.edu
```

