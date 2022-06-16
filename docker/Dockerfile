FROM debian:bullseye-slim


RUN apt-get update 

RUN apt-get install --assume-yes --no-install-recommends --quiet \
    python3 \
    python3-pip \
    ffmpeg \
    libsndfile1-dev

RUN pip install --no-cache --upgrade pip setuptools

RUN pip3 install numpy \
    scikit-learn \
    torch \
    nltk \
    matplotlib \
    h5py \
    opencv-python

FROM tensorflow/tensorflow:2.7.0-gpu

# Set working directory to MultiModalTVShowSeg-2022
WORKDIR /MultiModalTVShowSeg-2022

ADD ./requirements.txt .
ADD ./inaSpeechSegmenter .

# View contents while building dockerfile
RUN ls -a


RUN pip install --upgrade pip && pip install . && pip cache purge

# Install local dependencies
RUN pip install -r requirements.txt

# Install inaSpeechSegmenter dependencies
RUN cd inaSpeechSegmenter
RUN pip install .
RUN cd ..