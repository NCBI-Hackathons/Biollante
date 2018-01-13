# Dockerfile to build container to run Biollante software
FROM ubuntu:16.04

MAINTAINER Biollante <https://github.com/NCBI-Hackathons/PlantContam>

RUN  apt-get update \
  && apt-get install -y wget libxml2 \
  && rm -rf /var/lib/apt/lists/*

# install and configure
ADD https://github.com/NCBI-Hackathons/PlantContam/archive/master.zip /opt/biollante

# install python3 dependencies for dna2vec
RUN apt-get install python3-pip \
  && pip3 install -r /opt/biollante/dna2vec/requirements.txt \
  && pip install logbook xgboost sklearn keras tensorflow

# install Magic BLAST TODO may not be needed
RUN wget -P /opt/magicblast ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.3.0-x64-linux.tar.gz \
  && tar xzfv /opt/magicblast/ncbi-magicblast-1.3.0-x64-linux.tar.gz \
  && rm /opt/magicblast/ncbi-magicblast-1.3.0-x64-linux.tar.gz \
  && ln -s /opt/magicblast/ncbi-magicblast-1.3.0/bin/magicblast /usr/bin/magicblast

# environment variables
ENV LANG C.UTF-8

# ensure dna2vec is on the python path
ENV PYTHONPATH $PYTHONPATH:/opt/biollante/dna2vec

# default entrypoint
ENTRYPOINT ["/bin/bash"]
