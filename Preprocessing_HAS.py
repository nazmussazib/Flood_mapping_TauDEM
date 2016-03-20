__author__ = 'shams'


import os
from osgeo import gdal, ogr
import subprocess


def PreProcess_Height_Above_Stream(input_dir_name,watershed_shapefile,watershed_raster,droptostream_raster,dinfslope_raster):
    input_dir1=input_dir_name  #+"\\Main_Watershed"
    infile = input_dir_name+"\\"+watershed_shapefile

    ##if not os.path.exists(input_dir1):
    ##   os.makedirs(input_dir1)

    output_dir2=input_dir_name+"\\Subwatershed_ALL"
    if not os.path.exists(output_dir2):
       os.makedirs(output_dir2)

    main_dir=input_dir1;subwshed_file=watershed_raster;dts_file=droptostream_raster;dinfslope_file=dinfslope_raster
    # Get the input Layer
    inShapefile =infile
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(inShapefile, 0)
    inLayer = inDataSource.GetLayer()
    spatialRef = inLayer.GetSpatialRef()


# loop through input feature
    for i in range(0, inLayer.GetFeatureCount()):
        ## create directory
        ## TODO it may be better to label the subwatersheds with gridcode so that we do not need to do two lookups to find which folder to look in
      dest = output_dir2+"\\Subwatershed"+str(i)
      os.mkdir(dest)
# Get the input Feature
      inFeature = inLayer.GetFeature(i)
# Create output Feature
      os.chdir(dest)
       # Create the output Layer
      outShapefile =dest+"\\"+"subwatershed_"+str(i)+".shp"
      outDriver = ogr.GetDriverByName("ESRI Shapefile")

# Remove output shapefile if it already exists
      if os.path.exists(outShapefile):
          outDriver.DeleteDataSource(outShapefile)

# Create the output shapefile
      outDataSource = outDriver.CreateDataSource(outShapefile)
      outLayer = outDataSource.CreateLayer("subwatershed_"+str(i),  spatialRef ,geom_type=ogr.wkbPolygon)

# Add input Layer Fields to the output Layer
      inLayerDefn = inLayer.GetLayerDefn()
      for k in range(0, inLayerDefn.GetFieldCount()):
          fieldDefn = inLayerDefn.GetFieldDefn(k)
          outLayer.CreateField(fieldDefn)
    # Get the output Layer's Feature Definition
      outLayerDefn = outLayer.GetLayerDefn()
      outFeature = ogr.Feature(outLayerDefn)
# Add field values from input Layer
      for m in range(0, outLayerDefn.GetFieldCount()):
             outFeature.SetField(outLayerDefn.GetFieldDefn(m).GetNameRef(), inFeature.GetField(m))
# get geometry
      geom = inFeature.GetGeometryRef()

      outFeature.SetGeometry(geom)
# Add new feature to output Layer
      outLayer.CreateFeature(outFeature)
# close output file
      outDataSource.Destroy()
 ## open new output file for clipping
      infile = outShapefile
      inSource = inDriver.Open(infile, 0)
      inlayer = inSource.GetLayer()
      extent = inlayer.GetExtent()

      subwaterdir=os.path.join(main_dir,subwshed_file);subwater_out_file=os.path.join(dest,'subwatershed_'+str(i)+"w.tif")
      dtsdir=os.path.join(main_dir,dts_file);dts_out_file=os.path.join(dest,'subwatershed_'+str(i)+"dd.tif")
      dinfslpdir=os.path.join(main_dir,dinfslope_file);dinfslp_out_file=os.path.join(dest,'subwatershed_'+str(i)+"slp.tif")
      command_subw="gdalwarp -te " + str(extent[0]) + " " + str(extent[2]) + " " + str(extent[1]) + " " + str(extent[3]) + " -dstnodata -32768 -cutline " + outShapefile+ " -cl "+ "subwatershed_"+str(i)+ " " +  subwaterdir + " " + subwater_out_file
      command_dd="gdalwarp -te " +str(extent[0]) + " " + str(extent[2]) + " " + str(extent[1]) + " " + str(extent[3])+ " -dstnodata -32768 -cutline " + outShapefile+ " -cl "+ "subwatershed_"+str(i) + " " + dtsdir + " " + dts_out_file
      command_slp="gdalwarp -te " + str(extent[0]) + " " + str(extent[2]) + " " + str(extent[1]) + " " + str(extent[3])+ " -dstnodata -32768 -cutline " +outShapefile + " -cl "+ "subwatershed_"+str(i) + " " +  dinfslpdir + " " + dinfslp_out_file

      print(command_subw)
      subprocess.check_call(command_subw)
      subprocess.check_call(command_dd)
      subprocess.check_call(command_slp)


# Close DataSources
    inDataSource.Destroy()
    #outDataSource.Destroy()











