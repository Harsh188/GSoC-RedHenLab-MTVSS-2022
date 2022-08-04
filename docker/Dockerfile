# Create base OS Image
# FROM debian:bullseye-slim AS base
FROM tensorflow/tensorflow:2.9.0-gpu

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
    openssh-client \
    libavcodec-dev \
    libavfilter-dev \
    libavformat-dev \
    libavutil-dev \
    libsndfile1-dev

# Image layer on top of base to install requirements
# FROM tensorflow/tensorflow:2.9.0-gpu

# Set working directory to MultiModalTVShowSeg-2022
WORKDIR /MultiModalTVShowSeg-2022

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

## INSTALL DECORD
# official PPA comes with ffmpeg 2.8, which lacks tons of features, we use ffmpeg 4.0 here
RUN sudo add-apt-repository ppa:jonathonf/ffmpeg-4 # for ubuntu20.04 official PPA is already version 4.2, you may skip this step
RUN sudo apt-get install -y python3-setuptools make cmake
# note: make sure you have cmake 3.8 or later, you can install from cmake official website if it's too old

RUN cd decord
RUN mkdir build && cd build
RUN cmake .. -DUSE_CUDA=0 -DCMAKE_BUILD_TYPE=Release
RUN make

