# Dockerfile for running lost in space and time

# pull base image
FROM python:3.6

# Install.
RUN \
  apt-get update && \
  apt-get install -y --no-install-recommends git \
  python3 \
  python3-pip \
  python3-all-dev \
  build-essential && \
  rm -rf /var/lib/apt/lists/*

#Update pip
RUN \
  pip3 install --upgrade pip &&\
  mkdir -p /usr/local/var/lispat

#Set our spacy as a env variable
ENV SPACY_VERSION 2.0.3

#Update the Image to include some program dependencies that are required for each other.
RUN \
  pip3 install -U numpy\
  pandas\
  requests\
  chardet\
  cffi\
  && pip3 install -U spacy==${SPACY_VERSION}\
  && python3 -m spacy download en

#Set environment variable for home
ENV HOME /root

#Add each directoy to the image.
ADD . /root/

#Set the working directory to root.
WORKDIR /root

#Run the setup.py to set our entry point and any lasting dependencies.
RUN python3 setup.py install && \
    chmod 777 /usr/local/var/lispat/


#Give the starting argument as lispat for the container.
ENTRYPOINT ["lispat"]
