"""
Read/Write OGR functions
"""
from osgeo import ogr
import sys

def openToRead(shapefile):
    driver = ogr.GetDriverByName("SQLite")
    if driver.Open(shapefile, 0):
        dataSource = driver.Open(shapefile, 0)
    else:
        print("Not possible to open the file "+shapefile)
        sys.exit(1)
    return dataSource

def openToReadWrite(shapefile):
    driver = ogr.GetDriverByName("SQLite")
    if driver.Open(shapefile, 1):
        dataSource = driver.Open(shapefile, 1)
    else:
        print("Not possible to open the file "+shapefile)
        sys.exit(1)
    return dataSource
