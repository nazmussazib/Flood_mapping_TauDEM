
__author__ = 'shams'
import os
from Preprocessing_HAS import *

input_dir_name=r'E:\USU_Research_work\NFIE_Flood_Mapping\Onion'
watershed_shapefile='onionwatershed_diss.shp'
watershed_raster='Onionw.tif'
droptostream_raster="Oniondd.tif"
dinfslope_raster="Onionslp.tif"


PreProcess_Height_Above_Stream(input_dir_name,watershed_shapefile,watershed_raster,droptostream_raster,dinfslope_raster)
