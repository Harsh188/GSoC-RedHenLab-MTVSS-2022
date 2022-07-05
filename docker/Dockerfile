# Create base OS Image
# FROM debian:bullseye-slim AS base
FROM tensorflow/tensorflow:2.9.0-gpu

# Update the OS image
RUN apt-get -y update 

# Install packages
RUN apt-get install -y --no-install-recommends --quiet \
    python3 \
    python3-pip \
    ffmpeg \
    rsync \
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

# Install inaSpeechSegmenter dependencies
RUN cd inaSpeechSegmenter
RUN pip3 install .
RUN cd ..

# Remove inaSpeechSegmenter
RUN rm -f -r ./inaSpeechSegmenter