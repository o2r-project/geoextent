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
def get_list_of_records(term,mb_size):
    
    size = mb_size*1000000
    
    response_hits = requests.get('https://zenodo.org/api/records/',
                              params={'q':str(term),
                                      "access_right":"open",
                                      "size" : "1",
                                     "type":"dataset"})
    hits = response_hits.json()['hits']['total']
    
    print("{} repositories found for '{}' query search term".format(hits,term))
    zenodo_ids = []
    
    if hits > 0 :
        
        response = requests.get('https://zenodo.org/api/records/',
                              params={'q':'geo',"access_right":"open","size" : str(hits),"type":"dataset"})
        
        content = response.json()

    for i in range(0,hits):
        if content['hits']['hits'][i]['files'][0]['size']<= size:  
            zenodo_ids.append(content['hits']['hits'][i]['conceptrecid'])
    
    print("{} out of {} repositories smaller than {} MB".format(len(zenodo_ids),hits,mb_size))
        
    return zenodo_ids



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
        print(zenodo_id)
        file = tmp_dir+str(zenodo_id)+".txt"
        zget.zenodo_get([str(zenodo_id),"-w",file])
        command = 'wget -i ' + file +" -P " + tmp_dir
        os.system(command)
        f = geoextent.fromDirectory(tmp_dir, True, True)
        geo_extent = {'id':zenodo_id,'geoextent':f}
        
    return geo_extent


geo = get_list_of_records("geo",100)

# +
repository_list = geo[1:10]
results = {}

for i in repository_list:
    results[i] = zenodo_geoextent(i)
    
# -

results

# ### Geoextent 

#
#

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
