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
docker run --gpus all -it --rm -p 8888:8888 -v $PWD:/MultiModalTVShowSeg-2022
```

#### Jupyter Notebook

Once the container is up and running use the following code to launch jupyter notebooks.

```
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```