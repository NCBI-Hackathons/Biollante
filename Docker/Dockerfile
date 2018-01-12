# Dockerfile to build container to run Biollante software
FROM ubuntu:16.04

MAINTAINER Biollante <https://github.com/NCBI-Hackathons/PlantContam>

# environment variables
ENV LANG C.UTF-8

# install and configure
ADD https://github.com/NCBI-Hackathons/PlantContam/archive/master.zip /opt/biollante

# install python3 dependencies for dna2vec
RUN bash apt-get install python3-pip
RUN bash pip3 install -r /opt/biollante/dna2vec/requirements.txt

# ensure dna2vec is on the python path
ENV PYTHONPATH $PYTHONPATH:/opt/biollante/dna2vec

# default entrypoint
ENTRYPOINT ["/bin/bash"]
