FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
	software-properties-common

# To get necessary dependencies for gdal-bin
RUN add-apt-repository ppa:ubuntugis/ppa 

# Install required libraryes including GDAL development libraries
RUN apt-get update && apt-get install -y \
	sudo\
	python3.6\
	python3-pip\
	python3.6-dev\
	gdal-bin\
	libgdal-dev

COPY requirements.txt /requirements.txt

# Install required libraryes including geoextent and GDAL
RUN pip3 install gdal==$(gdal-config --version) \
	-r requirements.txt \
	geoextent \
	--no-cache-dir notebook==6.0.3 \
	bash_kernel

# Install Jupyter kernel for bash
RUN python3 -m bash_kernel.install 

# Create a user
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

# Make contents available to users
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}