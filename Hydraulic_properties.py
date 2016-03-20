__author__ = 'shams'
## this code calculates hydraulic properties for
import os

from osgeo import gdal,ogr
import pandas as pd
import numpy as np
import numpy.ma as ma

## inputs
## change the inputs
input_dir_name=r'D:\Dropbox\Projects\CUAHSI\Collaboration\NFIE\NationalInundation\Onion\TauDEM' ## directory where "Main_watershed" is located
## please check whether all input files are located inside the "Main_Watershed" directory
watershed_file='onionwd.shp'
streamnetfile='Onionnet.shp'



networkfile = input_dir_name+"\\"+streamnetfile
output_dir2=input_dir_name+"\\Subwatershed_ALL"
infile = input_dir_name+"\\"+watershed_file
myheight = [0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.5,4,4.5,5,5.5,6,7,8,9,10]
inShapefile =infile
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(inShapefile, 0)
inLayer = inDataSource.GetLayer()
NetworkDataSource = inDriver.Open(networkfile, 0)
NetworkLayer = NetworkDataSource.GetLayer()


# Add features to the ouput Layer
for i in range(0, inLayer.GetFeatureCount()):

    length_all=[]
    area_all=[]
    volume_all=[]
    bed_all=[]
    dir=output_dir2+"\\Subwatershed"+str(i)
    feature =NetworkLayer.GetFeature(i)
    length = feature.GetField("Length")
    os.chdir(dir)
    inputfn = 'subwatershed_'+str(i)+'.csv'                ##input file name

    dts_file=os.path.join(dir,'subwatershed_'+str(i)+"dd.tif")
    dinfslp_file=os.path.join(dir,'subwatershed_'+str(i)+"slp.tif")

    dts_ds = gdal.Open(dts_file)
    band_dts =dts_ds.GetRasterBand(1)
    nodata_dts = band_dts.GetNoDataValue()
    array_dts =band_dts.ReadAsArray()
    arraydts = ma.masked_where(array_dts==nodata_dts, array_dts)
        # ##calcualte average slope
    slope_ds = gdal.Open(dinfslp_file)
    array_slp= np.array(slope_ds.GetRasterBand(1).ReadAsArray())
    bandslp = slope_ds.GetRasterBand(1)
    nodataslp = bandslp.GetNoDataValue()
    arrayslp = ma.masked_where(array_slp==nodataslp, array_slp)


    for k in range (0,len(myheight)):

      length=round(length,2)
      length_all.append(length)
      dts_value= arraydts-myheight[k] ## subtract height from distance raster
      dts_less_height=dts_value<0 # find dts<0
      count_cell=dts_less_height.sum() ## ## count number of cell has less than zero
     # count_cell=len(arraydts[dts_less_height]) ## provied only row number which is not true
      Area=count_cell*8.92*10.29 ## in m2
      Area=round(Area,2)
      area_all.append(Area)
      cell_height=dts_value[dts_less_height]*(-1)
      volume_in=8.92*10.29*cell_height ## volume
      volume=volume_in.sum()
      volume=round(volume,2)
      volume_all.append(volume)
      slp=arrayslp[dts_less_height]*arrayslp[dts_less_height]
      #print(slp)
      slp1=slp+1.0
      #print(slp1)
      bed_area_all1=np.sqrt(slp1)
      bed_area_all2= bed_area_all1*8.92*10.29 ##
      bed_area=bed_area_all2.sum()
      bed_area=round(bed_area,2)
      bed_all.append(bed_area)
    raw_data = {'Height(m)':myheight,
                'Length(m)': length_all,
                 'Area(m2)': area_all,
                'Volume(m3)': volume_all,
               'Bed Area(m2)': bed_all }
               # 'postTestScore': [25, 94, 57, 62, 70]}
    my_df = pd.DataFrame(raw_data,columns = ['Height(m)','Length(m)','Area(m2)','Volume(m3)','Bed Area(m2)'])
    my_df.to_csv(inputfn,index=False,header=True)






