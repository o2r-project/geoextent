FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
	software-properties-common

# To get necessary dependencies for gdal-bin
RUN add-apt-repository ppa:ubuntugis/ppa 

RUN apt-get update

# Install required libraryes including GDAL development libraries
RUN apt-get update && apt-get install -y \
	sudo\
	python3.6\
	python3-pip\
  	python3-gdal \
	gdal-bin\
	libgdal-dev

RUN ogrinfo --version

COPY requirements.txt /requirements.txt

RUN pip3 install --upgrade setuptools pip

# Install required libraryes including geoextent and GDAL
RUN pip3 install pygdal==$(gdal-config --version).* \
	-r requirements.txt \
	--no-cache-dir notebook==6.0.3 \
	bash_kernel

# Install Jupyter kernel for bash
RUN python3 -m bash_kernel.install

COPY showcase/requirements.txt /requirements-showcase.txt

RUN pip3 install -r requirements-showcase.txt

RUN pip3 install geoextent

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
WORKDIR ${HOME}
