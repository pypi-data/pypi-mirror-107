# Pointcloudpipeline

A simple commandline app for managing pointclouds in LAZ. There are functions to get a laz out of e57, ply or las as well as a function to convert laz back to e57, ply or las and these will show you all the metadata on your commandline. You also can convert pointclouds into a viewable Entwine format or into a 2D raster.

If you want to use the functionality as import in a project and not as a commandline app you can use the functions over the import statement.

# Installation

## Preparation
1. Install Python and pipenv
   ```
   $ sudo apt install python3
   $ sudo apt install python3-pip
   $ sudo apt install pipenv
   ```
2. Install git
   ```
   $ sudo apt install git
   ```
3. Install PDAL for converting point clouds
   ```
   $ sudo apt install libpdal-dev
   $ sudo apt install cmake
   $ sudo apt install pdal
   $ pdal --version (should be min 2.1 or higher, but not 2.0.1)
   ```
4. Install untwine https://github.com/hobu/untwine.git anywhere you want. Later you need only the path to the entwine build data. (Example: /home/user/Documents/original/untwine/build/entwine)
   ```
   $ git clone https://github.com/hobu/untwine.git
   $ cd untwine
   $ mkdir build
   $ cd build
   $ cmake ..
   $ make
   ```

## Manual installation Pointbrowserpipline
```
  $ git clone https://gitlab.ost.ch/nadine.sennhauser/pointcloudpipeline
  $ cd pointcloudpipeline
  $ pipenv shell
  $ pipenv install
  $ python setup.py install
```

## Using Pip
```
  $ pip install pointcloudpipeline
```

# Usage

## As a commandline tool
Functions:
* convertfromlaz: Convert a LAZ-pointcloud to desired type.
  * Options:
    * --lazFile TEXT: LAZ-file to convert  [required]
    * --directoryTo TEXT: Directory to save converted file
    * --convertTo [las|laz|e57|ply]: Desired filetype
    * --help: Show help

* convertlazto2d: Convert LAZ to a top rasterview in 2D.
  * Options: 
    * --lazFile TEXT: LazFile to convert  [required]
    * --directoryTo TEXT: Directory to save
    * --help: Show help

* convertlaztoeptlaz: Convert a pointcloud from LAZ to EPT-LAZ.
  * Options:
    * --lazFile TEXT: LazFile to convert  [required]
    * --directoryTo TEXT: Directory to save
    * --untwinePath TEXT: Path to untwine
    * --help: Show help.

* converttolaz: Convert a pointcloud from ['las', 'laz', 'e57', 'ply'] to LAZ and save it.
  * Options:
    * --file TEXT: File to convert to LAZ  [required]
    * --directoryTo TEXT: Directory to save LAZ
    *  --help: Show help.


Options:
* --version: Show the version and exit.
* --help: Show this message and exit.

Example:
```
  $ pointcloudpipeline convertlazto2d --lazFile /home/hacker/Documents/original/pointcloudpipeline/test_data/from/test.laz --directoryTo /home/hacker/Documents/original/pointcloudpipeline/test_data/to

{
  "metadata":
  {
    "readers.las":
    {
      "comp_spatialreference": "",
      "compressed": true,
      "count": 1843780,
      "creation_doy": 119,
      "creation_year": 2021,
      "dataformat_id": 2,
      "dataoffset": 327,
      "filesource_id": 0,
      "global_encoding": 0,
      "global_encoding_base64": "AAA=",
      "header_size": 227,
      "major_version": 1,
      "maxx": 33.4728,
      "maxy": 39.8786,
      "maxz": 9.5308,
      "minor_version": 2,
      "minx": -72.9241,
      "miny": -19.287,
      "minz": -1.1721,
      "offset_x": 0,
      "offset_y": 0,
      "offset_z": 0,
      "point_length": 26,
      "project_id": "00000000-0000-0000-0000-000000000000",
      "scale_x": 0.0001,
      "scale_y": 0.0001,
      "scale_z": 0.0001,
      "software_id": "GeoSLAM",
      "spatialreference": "",
      "srs":
      {
        "compoundwkt": "",
        "horizontal": "",
        "isgeocentric": false,
        "isgeographic": false,
        "prettycompoundwkt": "",
        "prettywkt": "",
        "proj4": "",
        "units":
        {
          "horizontal": "unknown",
          "vertical": ""
        },
        "vertical": "",
        "wkt": ""
      },
      "system_id": "libLAS",
      "vlr_0":
      {
        "data": "AgAAAAIAAgAAAAAAUMMAAP////////////////////8CAAYAFAACAAgABgACAA==",
        "description": "http://laszip.org",
        "record_id": 22204,
        "user_id": "laszip encoded"
      }
    },
    "writers.gdal":
    {
      "filename":
      [
        "/home/hacker/Documents/original/pointcloudpipeline/test_data/to/test.tif"
      ]
    }
  }
}
```
## As import in other projects
```Python
from pipeline import pipeline_worker
```
Functions:
* convertLazToEPTLaz(lazFile, directoryTo, untwinePath)
* convertToLaz(file, directoryTo)
* convertFromLaz(lazFile, directoryTo, typeOut)
* convertLAZTo2D(lazFile, directoryTo)

Example:
```Python
pipelineworker.convertLAZto2D(/home/Documents/original/pointcloudpipeline/test_data/test.laz /home/hacker/Documents/original/pointcloudpipeline/test_data/to)
```
