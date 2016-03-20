
__author__ = 'shams'
import os
from Preprocessing_HAS import *


## change all inputs

input_dir_name=r'D:\Dropbox\Projects\CUAHSI\Collaboration\NFIE\NationalInundation\Onion\TauDEM' ##  where "Main_Watershed"  is located
## please check whether all input files are located inside the "Main_Watershed" directory
## TODO Set up so that these inputs are also used for Hydraulic properties
watershed_shapefile='onionwd.shp' ##
watershed_raster='Onionw.tif'
droptostream_raster="Oniondd.tif"
dinfslope_raster="Onionslp.tif"
PreProcess_Height_Above_Stream(input_dir_name,watershed_shapefile,watershed_raster,droptostream_raster,dinfslope_raster)
# TODO put the hydraulic properties calculation as a function here so one function does all
