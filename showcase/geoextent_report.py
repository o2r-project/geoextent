# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Report Geoextent

# Ideas for 'abstract'
#
# Academics studies generally include a geographical extent.
#
# Academic repositories store all kind of files that allow reasearchers to share information about their investigations. Some of those files include the analyzed datasets or the code used for their analysis. In this regard, the files available in each repositority include not only the information of individual measurements or methods but multiple information as the temporal or spatial extent of the studies. 
#
# Temporal and spatial extent are properties that are present in almost all studies, however while searching for public repositories by an spatial component this query is most of the time limited to key words (e.g. name of countries). 
#
# Multiple types of data -> hard to define a geographic extension
#
#
# Objective: 
#
# Extract geographycal extent of academic repositories.

# # Introduction

# ## Database extraction

# These sets of functions download databases by using their DOI from four academic repositories. The functions also extracts the metadata of the database (e.g., location if available).

# ### DOI to repository identification

# +
#TODO
# This functions use as an input the DOI of a dataset and returns the name of the academic repository where it
# is hosted (Zenodo,Figshare,GFZ Data Services, Pangaea) and their ID in the corresponding repository.
# -

# #### Zenodo
# ##### Getting list of records
# The following method extracts all the zenodo ids from an specific search term.

import requests
import json
def get_list_of_records(term,mb_size):
    
    response_hits = requests.get('https://zenodo.org/api/records/',
                              params={'q':str(term),
                                      "access_right":"open",
                                      "size" : "1",
                                     "type":"dataset"})
    hits = response_hits.json()['hits']['total']
    
    print("{} repositories found for '{}' query search term".format(hits,term))
    zenodo_search = {}
    
    if hits > 0 :
        
        response = requests.get('https://zenodo.org/api/records/',
                              params={'q':'geo',"access_right":"open","size":str(hits),"type":"dataset"})
        
        content = response.json()

    for i in range(0,hits):
        
        files = content['hits']['hits'][i]['files']
        size = round(sum(f['size'] for f in files)/2 **20,1)
        if size <= mb_size:
            record_id = content['hits']['hits'][i]['conceptrecid']
            doi = content['hits']['hits'][i]['doi']
            title = content['hits']['hits'][i]['metadata']['title']
            license = content['hits']['hits'][i]['metadata']['license']['id']
            zenodo_search[record_id] = {"doi":doi,"title":title,"license":license,"size_mb":size}
    print("{} out of {} repositories smaller than {} MB".format(len(zenodo_search),hits,mb_size))

    return zenodo_search


# #### Figshare
#

# +
#TODO

# This function downloads a Figshare repository and extracts the available metadata
# -

# #### GFZ Data Services

# +
#TODO

# This function downloads a GFZ Data Services repository and extracts the available metadata
# -

# #### Pangaea

# +
#TODO

# This function downloads a Pangaea repository and extracts the available metadata
# -

# ### Geographic extent

# These sets of functions iterate through the repositories and extract the geospatial information.

# 1. If an extent is found (or if not = NA), Add record URL, ID, and some record metadata (names of contained files, author, repository URL, license, ...),  and the resulting extent in WKT in a local "database" in GeoPackage format.
#
# 2. If not extent is found, store the record as visited and the list of filenames in a second data file

import geoextent.lib.extent as geoextent
import zenodo_get as zget
import tempfile
import os 


def zenodo_geoextent(zenodo_id):
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_dest = os.path.join(tmp_dir,str(zenodo_id))
        zget.zenodo_get([str(zenodo_id),"-e","-o",tmp_dir_dest])
        f = geoextent.fromDirectory(tmp_dir_dest, True, True, True)
        geo_extent = f
        
    return geo_extent


# ### Geoextent 

# +
#Get list of records
geo  = get_list_of_records("geo",mb_size=100)

subset_list = list(geo.keys())[1:5]
subset = {key: geo[key] for key in geo.keys() if key in subset_list}

for i in subset:
    if geoextent is not None:
        subset[i]['geoextent'] = zenodo_geoextent(i)

# +
import sys
import pandas as pd

def rep_to_table(dict_geo):
    
    repository_id = []
    title = []
    doi = []
    license = []
    tbox = []
    bbox = []
    crs = []
    
    for i in dict_geo:

        repository_info = dict_geo[i]
        repository_id.append(i)
        title.append(repository_info.get('title'))
        doi.append(repository_info.get('doi'))
        license.append(repository_info.get('license'))
        geoextent = repository_info.get('geoextent')
        tbox.append(geoextent.get('tbox'))
        bbox.append(geoextent.get('bbox'))
        crs.append(geoextent.get('crs'))
        
    d = {'repository_id': repository_id, 'title': title, 'doi':doi,'license':license,
        'bbox':bbox,'tbox':tbox,'crs':crs}
    
    repositories = pd.DataFrame(d)
    
    return repositories
        


# -

rep_to_table(subset)

# +
import os
import itertools

def extract_details(details,repository=1):
    
    filename = []
    file_format = []
    handler = []
    bbox = []
    tbox = []
    crs = []
    
    for i in details:
    
        file = details[i]
        
        if file is None:
            filename.append([i])
            file_format_v = os.path.splitext(i)[1][1:]
            if file_format_v is '':
                file_format_v = 'undetected'
            file_format.append([file_format_v])
            handler.append([None])
            bbox.append([None])
            tbox.append([None])
            crs.append([None])
        else:
            filename.append([i])
            file_format.append([file.get('format')])    
            handler_v = file.get('geoextent_handler')
            bbox_v = file.get('bbox')
            tbox_v = file.get('tbox')
            crs_v = file.get('crs')
            handler.append([handler_v])
            bbox.append([bbox_v])
            tbox.append([tbox_v])
            crs.append([crs_v])
            
            if file.get('format')=='folder':
                dictio = extract_details(file['details'])
                filename.append(dictio['filename'])
                file_format.append(dictio['format'])
                handler.append(dictio['handler'])
                bbox.append(dictio['bbox'])
                tbox.append(dictio['tbox'])
                crs.append(dictio['crs'])
    
    if any(isinstance(i, list) for i in filename):
        filename = list(itertools.chain.from_iterable(filename))
        file_format=  list(itertools.chain.from_iterable(file_format))
        handler = list(itertools.chain.from_iterable(handler))
        bbox= list(itertools.chain.from_iterable(bbox))
        tbox = list(itertools.chain.from_iterable(tbox))
        crs = list(itertools.chain.from_iterable(crs))
        
    d = {'filename': filename, 'format': file_format, 'handler':handler,'bbox':bbox,'tbox':tbox,'crs':crs}
    
    return(d)


# -

def file_table(subset):
    
    filename = []
    file_format = []
    handler = []
    tbox = []
    bbox = []
    crs = []
    
    for rep in subset:

        file = subset[rep]['geoextent']['details']
        repository = extract_details(file,1)

        filename.append(repository.get('filename'))
        file_format.append(repository.get('format'))
        handler.append(repository.get('handler'))
        tbox.append(repository.get('tbox'))
        bbox.append(repository.get('bbox'))
        crs.append(repository.get('crs'))

    if any(isinstance(i, list) for i in filename):
            
        filename = list(itertools.chain.from_iterable(filename))
        file_format=  list(itertools.chain.from_iterable(file_format))
        handler = list(itertools.chain.from_iterable(handler))
        bbox= list(itertools.chain.from_iterable(bbox))
        tbox = list(itertools.chain.from_iterable(tbox))
        crs = list(itertools.chain.from_iterable(crs))

    d = {'filename': filename, 'format': file_format, 'handler':handler,'bbox':bbox,'tbox':tbox,'crs':crs}
    files = pd.DataFrame(d)
    return(files)
   


file_table(subset)

# # Results

# **GRAPH 1: Proportion of repositories with geospatial metadata**

# +
# NUMBER OF REPOSITORIES WITH GEOSPATIAL METADATA / NUMBER OF REPOSITORIES
# what do they answer? 
# Proportion of repositories with geospatial metadata
# -

# **GRAPH 2: Proportion of repositories with successful geospatial extraction (Geoextent)**

# +
# NUMBER OF REPOSITORIES WITH SUCCESSFULL GEOSPATIAL EXTRACTION / NUMBER OF REPOSITORIES
# what do they answer? 
# Does geoextent allow to extract geospatial information from repositories in a higher proportion that current metadata ?
# -

# **GRAPH 3: Distribution of files in repositories with successful geospatial extraction (Geoextent)**

# +
# DISTRIBUTION OF FILES IN SUCCESSFUL GEOSPATIAL EXTRACTION
# what do they answer?
# What types of files (supported by geoextent) are more popular in the repositories ?
# -

# **GRAPH 4: Distribution of (geo)files in repositories with unsuccessful geospatial extraction (Geoextent)**

# +
# DISTRIBUTION OF FILES IN UNSUCCESSFUL GEOSPATIAL EXTRACTIONS
# what do they answer?
# What type of files (geo but not supported by geoextent) are more popular in the repositories?
