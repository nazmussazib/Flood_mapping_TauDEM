__author__ = 'shams'
## this code calculates hydraulic properties for
import os

from osgeo import gdal
import fiona
import geopandas as gepan
import pandas as pd
import numpy as np
import numpy.ma as ma

## inputs:
input_dir_name=r'E:\USU_Research_work\NFIE_Flood_Mapping\Onion'
watershed_file='onionwatershed_diss.shp'
output_dir2=input_dir_name+"\\Subwatershed_ALL"
infile = input_dir_name+"\\Main_Watershed\\"+watershed_file
networkfile = input_dir_name+"\\Main_Watershed\\Onionnet.shp"



boros = gepan.GeoDataFrame.from_file(networkfile)
df=pd.DataFrame(boros)
myheight = [0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.5,4,4.5,5,5.5,6,7,8,9,10]
with fiona.open(infile) as source:



       for f in source:
            #print(f)
            length_all=[]
            area_all=[]
            volume_all=[]
            bed_all=[]
            dir=output_dir2+"\\Subwatershed"+str(f['properties']['GRIDCODE'])
            os.chdir(dir)
            inputfn = 'subwatershed_'+str(f['properties']['GRIDCODE'])+'.csv'                ##input file name

            dts_file=os.path.join(dir,'subwatershed_'+str(f['properties']['GRIDCODE'])+"dd.tif")
            dinfslp_file=os.path.join(dir,'subwatershed_'+str(f['properties']['GRIDCODE'])+"slp.tif")
            src_file=os.path.join(dir,'subwatershed_'+str(f['properties']['GRIDCODE'])+"src1.tif")

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


            for i in range (0,len(myheight)):
              mask = df[['WSNO']].isin([f['properties']['GRIDCODE']]).all(axis=1)
              data_mask=df.ix[mask]
              length=np.array(data_mask['Length'])[0] ## get length
              length=round(length,2)
              length_all.append(length)


              dts_value= arraydts-myheight[i] ## subtract height from distance raster
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






