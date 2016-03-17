__author__ = 'shams'
__author__ = 'shams'

import shutil
import os
import fiona
from osgeo import gdal
import glob
import subprocess


def PreProcess_Height_Above_Stream(input_dir_name,watershed_shapefile,watershed_raster,droptostream_raster,dinfslope_raster):
    input_dir1=input_dir_name+"\\Main_Watershed"
    infile = input_dir1+"\\"+watershed_shapefile
    output_dir1=input_dir_name+"\\Subwatershed"
    if not os.path.exists(input_dir1):
       os.makedirs(input_dir1)
    if not os.path.exists(output_dir1):
       os.makedirs(output_dir1)
    output_dir2=input_dir_name+"\\Subwatershed_ALL"
    if not os.path.exists(output_dir2):
       os.makedirs(output_dir2)


    with fiona.open(infile) as source:
        meta = source.meta
        for f in source:
            dest = output_dir1
            outfile = os.path.join(dest, "subwatershed_%s.shp" % f['properties']['GRIDCODE'])
            with fiona.open(outfile, 'w', **meta) as sink:
                sink.write(f)


# # make directory for each of the subwatershed and then extract and keep subwatershed, complimentary watershed shapefile
    with fiona.open(infile) as source:
       source_dir=output_dir1
       os.chdir(source_dir)
       for f in source:
        dest = output_dir2+"\\Subwatershed"+str(f['properties']['GRIDCODE'])
        os.mkdir(dest)
        sub=os.path.join(source_dir,"subwatershed_"+str(f['properties']['GRIDCODE'])+".*")
        files_sub=glob.glob(sub)
        for file1 in files_sub:
            if os.path.isfile(file1):
                shutil.copy2(file1, dest)




#
# # extract streamraster,flow direction, watershed grid for each of the subwateshed and store in the subwatershed directory
    with fiona.open(infile) as source:
       for f in source:
            dir=output_dir2+"\\Subwatershed"+str(f['properties']['GRIDCODE'])
            os.chdir(dir)
            inputfn = 'subwatershed_'+str(f['properties']['GRIDCODE'])+'.shp'                ##input file name

            main_dir=input_dir1;subwshed_file=watershed_raster;dts_file=droptostream_raster;dinfslope_file=dinfslope_raster
            subwaterdir=os.path.join(main_dir,subwshed_file);subwater_out_file=os.path.join(dir,'subwatershed_'+str(f['properties']['GRIDCODE'])+"w.tif")
            dtsdir=os.path.join(main_dir,dts_file);dts_out_file=os.path.join(dir,'subwatershed_'+str(f['properties']['GRIDCODE'])+"dd.tif")
            dinfslpdir=os.path.join(main_dir,dinfslope_file);dinfslp_out_file=os.path.join(dir,'subwatershed_'+str(f['properties']['GRIDCODE'])+"slp.tif")

            input = fiona.open(inputfn, 'r')
            xmin=str(input.bounds[0])
            ymin=str(input.bounds[1])
            xmax=str(input.bounds[2])
            ymax=str(input.bounds[3])
            layer_name=os.path.splitext(inputfn)[0]

            command_subw="gdalwarp -te " + xmin + " " + ymin + " " + xmax + " " + ymax + " -dstnodata -32768 -cutline " + inputfn + " -cl "+ layer_name + " " +  subwaterdir + " " + subwater_out_file
            command_dd="gdalwarp -te " + xmin + " " + ymin + " " + xmax + " " + ymax + " -dstnodata -32768 -cutline " + inputfn + " -cl "+ layer_name + " " + dtsdir + " " + dts_out_file
            command_slp="gdalwarp -te " + xmin + " " + ymin + " " + xmax + " " + ymax + " -dstnodata -32768 -cutline " + inputfn + " -cl "+ layer_name + " " +  dinfslpdir + " " + dinfslp_out_file

            subprocess.check_call(command_subw)
            subprocess.check_call(command_dd)
            subprocess.check_call(command_slp)

            input.close()


# #Remove subwatershed directory which we dont need
    with fiona.open(infile) as source:
      for f in source:
        dest_dir=output_dir1
        shutil.rmtree(dest_dir,ignore_errors=True)








