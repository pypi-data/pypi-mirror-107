import os
import pdal
import numpy
import sys
import json
import subprocess

def convertLazToEPTLaz(lazFile, directoryTo, untwinePath):
    if not os.path.exists(lazFile):
        return lazFile + " does not exist."
    if not os.path.exists(untwinePath):
        return untwinePath + " does not exist."

    os.system(str(untwinePath) + ' --files=' + str(lazFile) + ' --output_dir=' + str(directoryTo) + '/' + os.path.splitext(os.path.basename(lazFile))[0])
    return str(untwinePath) + ' --files=' + str(lazFile) + ' --output_dir=' + str(directoryTo) + '/' + os.path.splitext(os.path.basename(lazFile))[0]

def convertToLaz(file, directoryTo):
    if os.path.exists(file):
        if(os.path.splitext(os.path.basename(file))[1]==".las" or os.path.splitext(os.path.basename(file))[1]==".laz"):
            readerType="readers.las"
        elif(os.path.splitext(os.path.basename(file))[1]==".e57"):
            readerType="readers.e57"
        elif(os.path.splitext(os.path.basename(file))[1]==".ply"):
            readerType="readers.ply"
        else:
            return file + " does not match the supported filetypes laz/las/e57/ply"
        jsonPipeline = {
            "pipeline": [
            {
                "type" : readerType,
                "filename" : file
            },
            {
                "type" : "writers.las", 
                "compression":"laszip",
                "filename" : directoryTo + "/" + os.path.splitext(os.path.basename(file))[0] + ".laz"
            }
            ]
            }
        pipeline = pdal.Pipeline(json.dumps(jsonPipeline))
        count = pipeline.execute()
        metadata = pipeline.metadata
        return metadata
    return file + " does not exist."

def convertFromLaz(lazFile, directoryTo, typeOut):
    if os.path.exists(lazFile):
        if(typeOut=="las"):
            writer = {
                "type" : "writers.las", 
                "filename" : directoryTo + "/" + os.path.splitext(os.path.basename(lazFile))[0] + ".las"
            }
        elif(typeOut=="e57"):
            writer = {
                "type" : "writers.e57", 
                "filename" : directoryTo + "/" + os.path.splitext(os.path.basename(lazFile))[0] + ".e57"
            }
        elif(typeOut=="ply"):
            writer = {
                "type" : "writers.ply", 
                "filename" : directoryTo + "/" + os.path.splitext(os.path.basename(lazFile))[0] + ".ply"
            }
        elif(typeOut=="laz"):
            writer = {
                "type": "writers.las", 
                "compression": "laszip",
                "filename" : directoryTo + "/" + os.path.splitext(os.path.basename(lazFile))[0] + ".laz"
            }
        else:
            return typeOut + " does not match supported the filetypes laz/las/e57/ply"
        jsonPipeline = {
            "pipeline": [
            {
                "type" : "readers.las",
                "filename" : lazFile
            },
            writer
        ]
        }
        pipeline = pdal.Pipeline(json.dumps(jsonPipeline))
        count = pipeline.execute()
        metadata = pipeline.metadata
        return metadata
    return lazFile + " does not exist."

def convertLAZTo2D(lazFile, directoryTo):
    if os.path.exists(lazFile):
        jsonPipeline = {
            "pipeline": [
            lazFile,
            {
                "type":"filters.outlier",
                "method":"statistical",
                "mean_k":"12",
                "multiplier":"1.0"
            },
            {
                "type":"filters.range",
                "limits":"Classification![7:7]"
            },
            {
                "filename":directoryTo + "/" + os.path.splitext(os.path.basename(lazFile))[0] + ".tif",
                "resolution":"0.05",
                "output_type":"max",
                "radius":"0.1",
                "type": "writers.gdal"
            }
            ]   
        }
        pipeline = pdal.Pipeline(json.dumps(jsonPipeline))
        count = pipeline.execute()
        metadata = pipeline.metadata
        return metadata
    return lazFile + " does not exist."
