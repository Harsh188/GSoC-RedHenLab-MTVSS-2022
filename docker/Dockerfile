# Create base OS Image
# FROM debian:bullseye-slim AS base
FROM tensorflow/tensorflow:2.9.0-gpu
# FROM nvcr.io/nvidia/tensorflow:22.07-tf2-py3

# Update the OS image
RUN apt-get -y update 

# Install packages
RUN apt-get install -y --no-install-recommends --quiet \
    build-essential \
    python3 \
    python3-pip \
    make \
    cmake \
    ffmpeg \
    rsync \
    python3-setuptools \
    openssh-client \
    libavcodec-dev \
    libavfilter-dev \
    libavformat-dev \
    libavutil-dev \

# Image layer on top of base to install requirements
# FROM tensorflow/tensorflow:2.9.0-gpu

# Set working directory to MultiModalTVShowSeg-2022
WORKDIR /MultiModalTVShowSeg-2022

# View contents while building dockerfile
RUN ls -a

ADD ./requirements.txt .
ADD ./inaSpeechSegmenter .

# View contents while building dockerfile
RUN ls -a

# Install local dependencies
RUN pip3 install -r requirements.txt

## INSTALL INASPEECHSEGMENTER
RUN cd inaSpeechSegmenter
RUN pip3 install .
RUN cd ..

# Remove inaSpeechSegmenter
RUN rm -f -r ./inaSpeechSegmenter
