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

# +
import requests
import json

def get_list_of_records(term,mb_size = False):
    
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
        
        if size <= mb_size or mb_size is False:
            record_id = content['hits']['hits'][i]['conceptrecid']
            doi = content['hits']['hits'][i]['doi']
            title = content['hits']['hits'][i]['metadata']['title']
            license = content['hits']['hits'][i]['metadata']['license']['id']
            zenodo_search[record_id] = {"doi":doi,"title":title,"license":license,"size_mb":size}
    
    if mb_size is not False:
        print("{} out of {} repositories smaller than {} MB".format(len(zenodo_search),hits,mb_size))

    return zenodo_search


# -

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
# 2. If not extent is found, store the record as visited and the list of filenames

import geoextent.lib.extent as geoextent
import zenodo_get as zget
import tempfile
import os
import sys
import pandas as pd
import geopandas as gpd
import shapely
from shapely.geometry import Polygon
from pyproj import CRS
import itertools
from itables import init_notebook_mode
init_notebook_mode(all_interactive=True)


# #### Geographic extent repositories

# This method extracts the repository information from the geoextent 'details' function output. The output is a dataframe with relevant features of each repository.

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
        
        if geoextent is not None:
            tbox.append(geoextent.get('tbox'))
            bbox.append(geoextent.get('bbox'))
            crs.append(geoextent.get('crs'))
        else:
            tbox.append(None)
            bbox.append(None)
            crs.append(None)
            
    def transform_bbox(x):
        try:
            bbox = shapely.geometry.box(*x)
        except:
            bbox = None    
        return bbox
    
    bbox = list(map(lambda x: transform_bbox(x) if x is not None else None,bbox))
    tbox = list(map(lambda x: str(x[0])+'/'+str(x[1]) if x is not None else None, tbox))
    d = {'repository_id': repository_id, 'title': title, 'doi':doi,'license':license,
        'bbox':bbox,'tbox':tbox,'crs':crs}
    
    repositories = pd.DataFrame(d)
  
    return repositories


# #### Geographic extract details

# This method extracts the file details from the geoextent 'details' function output for a **single folder**.

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
                
                details_folder = extract_details(file['details'],repository)
                filename.append(details_folder['filename'])
                file_format.append(details_folder['format'])
                handler.append(details_folder['handler'])
                bbox.append(details_folder['bbox'])
                tbox.append(details_folder['tbox'])
                crs.append(details_folder['crs'])
    
    if any(isinstance(i, list) for i in filename):
        filename = list(itertools.chain.from_iterable(filename))
        file_format=  list(itertools.chain.from_iterable(file_format))
        handler = list(itertools.chain.from_iterable(handler))
        bbox= list(itertools.chain.from_iterable(bbox))
        tbox = list(itertools.chain.from_iterable(tbox))
        crs = list(itertools.chain.from_iterable(crs))
        
    repository_id = [repository]*len(filename) 
    d = {'repository':repository_id,'filename': filename, 'format': file_format, 'handler':handler,'bbox':bbox,'tbox':tbox,'crs':crs}
    return d


# #### Geographic extract file details

# This method extracts the file details from the geoextent 'details' function output for **multiple folders** by using the _extract_details()_ function. The output is a dataframe with relevant features of each file.

def files_to_table(subset):
    
    filename = []
    rep_id = []
    file_format = []
    handler = []
    tbox = []
    bbox = []
    crs = []

    for rep in subset:

        geoextent = subset[rep]['geoextent']
        
        if geoextent is not None:
            details = geoextent.get('details')
            repository = extract_details(details,rep)
            rep_id.append(repository.get('repository'))
            filename.append(repository.get('filename'))
            file_format.append(repository.get('format'))
            handler.append(repository.get('handler'))
            tbox.append(repository.get('tbox'))
            bbox.append(repository.get('bbox'))
            crs.append(repository.get('crs'))
        else:
            filename.append([None])
            rep_id.append([rep])
            file_format.append([None])
            handler.append([None])
            tbox.append([None])
            bbox.append([None])
            crs.append([None])
            
    if any(isinstance(i, list) for i in filename):
        rep_id = list(itertools.chain.from_iterable(rep_id))
        filename = list(itertools.chain.from_iterable(filename))
        file_format =  list(itertools.chain.from_iterable(file_format))
        handler = list(itertools.chain.from_iterable(handler))
        bbox= list(itertools.chain.from_iterable(bbox))
        tbox = list(itertools.chain.from_iterable(tbox))
        crs = list(itertools.chain.from_iterable(crs))
        
    def transform_bbox(x):
        try:
            bbox = shapely.geometry.box(*x)
        except:
            bbox = None    
        return bbox
    
    bbox = list(map(lambda x: transform_bbox(x) if x is not None else None,bbox))
    tbox = list(map(lambda x: str(x[0])+'/'+str(x[1]) if x is not None else None, tbox))
    
    d = {'repository':rep_id,'filename': filename, 'format': file_format, 'handler':handler,'bbox':bbox,'tbox':tbox,'crs':crs}
    files = pd.DataFrame(d)
    
    return files


# ##### Download repository from zenodo and inspect geoextent

# This function downloads a repository by their **zenodo_id**, and then extract the geographical extent and temporal extent by using _geoextent_

# +
from IPython.utils import io

def zenodo_geoextent(zenodo_id):
    """
    
    
    
    """
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_dest = os.path.join(tmp_dir,str(zenodo_id))
        with io.capture_output() as captured:
            zget.zenodo_get([str(zenodo_id),"-e","-o",tmp_dir_dest])
        geo_extent = geoextent.fromDirectory(tmp_dir_dest, True, True, True)
        
    return geo_extent


# -

# ### Geoextent 

# +
#Get list of records

def geoextent_by_search_term_zenodo(term="geo",mb_size = False,output_path="geo_all.gpkg"):
    """ Extract geoextent of zenodo repositories base on a search term
    Keyword arguments:
    term -- search term (default "geo")
    mb_size -- mb size limit (double) defaul (False) if False there is no size limit
    output_path --  file name to return summary tables from extraction in a geopackage file

    """
    
    list_records = get_list_of_records(term,mb_size)
    num_repositories = len(list_records)
    error_ids = []
    counter = 1
    for i in list_records:
        print(str(counter)+" out of "+ str(num_repositories)+" repositories analyzed", end='\r')
        counter += 1
        try:
            list_records[i]['geoextent'] = zenodo_geoextent(i)
        except:
            list_records[i]['geoextent'] = None
            error_ids.append(i)
    
    try:
        repo = rep_to_table(list_records)     
        files = files_to_table(list_records)
        gdf_repo = gpd.GeoDataFrame(repo, geometry='bbox', crs=CRS("EPSG:4326"))
        gdf_files = gpd.GeoDataFrame(files, geometry='bbox', crs=CRS("EPSG:4326"))
        gdf_files.to_file(output, layer="files", driver="GPKG")
        gdf_repo.to_file(output, layer="repositories", driver="GPKG")

    except:
        print("Error exporting results into GeoPackage.")
        return list_records
    
    data = {"list_record":list_records,"error_ids":error_ids}
    
    return data


# +
import warnings
import logging
warnings.simplefilter("ignore")
logging.disable(sys.maxsize)

f = geoextent_by_search_term_zenodo(term="geo",mb_size = 0.1, output_path="geo_p1_mb.gpkg");
logging.disable(logging.NOTSET)
# -

# # Results

# After the extraction of geographical and temporal extent of zenodo repositories, the geopackage file is loaded to inspect the results. The geopackage contains two tables, the first one **repositories** and the second one **files**. The two tables are tied together by using the **repository_id** (repositories) and **repository** (for files) property.

# +
repositories_gdf = gpd.read_file("geo_200.gpkg",layer="repositories")
files_gdf = gpd.read_file("geo_200.gpkg",layer="files")

num_repositories = len(repositories_gdf)
num_files = len(files_gdf)

# File type 'folder' is removed to avoid repetition of information
index = files_gdf[files_gdf['format'] == 'folder'].index
files_gdf.drop(index, inplace=True)

# File 'md5sums.txt' file is removed as this file is included by zenodo in all of the repositories
index = files_gdf[files_gdf['filename'] == 'md5sums.txt'].index
files_gdf.drop(index, inplace=True)

# -

# ##### Results by repository

repositories_gdf[0:10]

# ##### Results by files

# +
from itables import show

files_gdf[20:30]

# As this table could contain thousends of entries, the fview is reduced. Is you want to display all the content, uncomment the following line:
# show(files_gdf, maxBytes=0)
# for more info : # https://mwouts.github.io/itables/#downsampling
# -

# ##### Bounding box 

# Visualization of bounding boxes

# +
import folium
from folium import plugins
from folium import  FeatureGroup, LayerControl
from folium.features import GeoJsonPopup 

# Extract only repositories and files with geometry

rep_valid = repositories_gdf[repositories_gdf.geometry.is_valid].copy().reset_index(drop=True)
files_valid = files_gdf[files_gdf.geometry.is_valid].copy().reset_index(drop=True)

m = folium.Map(max_bounds= True,height=500)
stripes = plugins.pattern.StripePattern(angle=-45,color="#f70707")
style = {'fillColor': '#f70707', 'color': '#f70707', 'dashArray': 5,'fillPattern' :stripes,'fillOpacity' : 0.6}   

for i in range(len(rep_valid)):
    fg = FeatureGroup(name=rep_valid["repository_id"][i]).add_to(m)
    folium.GeoJson(data = rep_valid["geometry"][i],
                   name = rep_valid["repository_id"][i],
                   style_function = lambda x: style,
                  ).add_child(
        folium.Popup(
            "<b> REPOSITORY </b>"+
            "<br><b> Repository ID: </b> " + rep_valid["repository_id"][i]+
            "<br><b> Title: </b> " + rep_valid["title"][i] + 
            "<br><b>   D.O.I: </b> </b>" + rep_valid["doi"][i]+
            "<br><b>  License: </b>" + rep_valid["license"][i]+
            "<br><b> tbox: </b>" + str(rep_valid["tbox"][i])
            ,max_width='250')).add_to(fg)


    
    for j in range(len(files_valid)):
        
        if files_valid["repository"][j]==rep_valid["repository_id"][i]:
            folium.GeoJson(data = files_valid["geometry"][j],
                        name = files_valid["repository"][j]).add_child(
                folium.Popup(
                    "<b> FILE </b>"+
                "<br><b> Repository ID of origin: </b> " + files_valid["repository"][j]+
                "<br><b> Filename: </b> " + files_valid["filename"][j]+  
                "<br><b> Format: </b> " + files_valid["format"][j] +
               "<br><b> Geoextent Handler: </b> " + str(files_valid["handler"][j]) 
                ,max_width='400')).add_to(fg)
    
LayerControl().add_to(m)
m
# -

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

# **GRAPH 3: Distribution of files in repositories**
#
# Distribution of files found in inspected repositories.

files_gdf['format'].value_counts().plot(kind='bar',
                                        title="File format distribution in repositories",
                                        figsize=(15,5),
                                        logy=True,
                                        fontsize=15)

# **GRAPH 4: Ocurrence of fileformat in repositories**
#
# Distribution of fileformats in repositories. Percentage of ocurrence of a fileformat in inspected repositories.

count = files_gdf.groupby(by=['format','repository']).count().groupby(by="format").count()['filename'].sort_values(ascending=False)/num_repositories*100
count.plot(kind='bar',
           title="File format distribution in repositories",
           xlabel = "Fileformat",
           ylabel = "Percentage of ocurrence",
           figsize=(15,5),
           fontsize=12)

# **GRAPH 5: Distribution of files in repositories with successful geospatial extraction (Geoextent)**

# +
d1 = pd.DataFrame({"Total":files_gdf['format'].value_counts()})
d2 = pd.DataFrame({"geoextent_success":files_valid['format'].value_counts()})
dj = d1.join(d2)
l = dj.dropna().copy()

l['perc_success'] = (l['geoextent_success']/l['Total'])*100

labels = l.index.values
success = l['perc_success']
failure = 100 - l['perc_success']

color_success = "#009900"
color_failure = "#FF3333"

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(15,4))
width = 0.35
ax.bar(labels, success, width, label='Successful',color= color_success)
ax.bar(labels, failure, width, bottom=success, color = color_failure,label='Failure')
ax.set_ylabel('Percentage',size=15)
ax.set_xlabel('geofile type',size=15)
ax.set_title('Geoextent extraction success by supported file type',size = 20)
ax.set_ylabel('Percentage')

count = 0
for bar in ax.patches: 

    displace =-1
    color = color_failure

    pos = 90
    
    if bar.get_y() == 0:
        
        n = l['Total'][count]
        count+=1
        displace = 3
        color= color_success
        pos = 0
        ax.annotate("n= "+str(n),  
                   (bar.get_x() + (bar.get_width()/2),  
                   50), ha='center', va='center', 
                   size=10, xytext=(0, 0),color='black', 
                   textcoords='offset points')
    
    ax.annotate(format(bar.get_height()/100, ".1%"),  
                   (bar.get_x() + (bar.get_width()*1.5),  
                   pos), ha='center', va='center', 
                   size=10, xytext=(0, 8),color=color, 
                   textcoords='offset points')
    
box = ax.get_position() 
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
ax.legend(loc='center right', bbox_to_anchor=(1.1, 0.5))

plt.show()
# -

# **GRAPH 6: Distribution of (geo)files in repositories with unsuccessful geospatial extraction (Geoextent)**

# +
# DISTRIBUTION OF FILES IN UNSUCCESSFUL GEOSPATIAL EXTRACTIONS
# what do they answer?
# What type of files (geo but not supported by geoextent) are more popular in the repositories?

#TODO:
#list of files with geoextent (potential source osgeo)
#geofiles = ['cal','csv','dbf','geojson','gff','gmt','gpkg','jpg','json','lyr','pdf','png','prj','shp','shx','tif','tfw','xml']
# -


