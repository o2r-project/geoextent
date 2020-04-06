FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
	software-properties-common

RUN add-apt-repository ppa:ubuntugis/ppa 

RUN apt-get update && apt-get install -y \
	sudo\
	python3.6\
	python3-pip\
	python3.6-dev\
	gdal-bin\
	libgdal-dev

COPY requirements.txt /requirements.txt

RUN pip3 install gdal==$(gdal-config --version) \
	-r requirements.txt \
	geoextent \
	--no-cache-dir notebook==6.0.3

ARG NB_USER=o2r
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

