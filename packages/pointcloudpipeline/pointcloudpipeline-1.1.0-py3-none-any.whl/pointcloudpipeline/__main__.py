import sys
import click
import os
from .pipeline_worker import convertToLaz, convertFromLaz, convertLazToEPTLaz, convertLAZTo2D

@click.group()
@click.version_option("1.0.0")
def main():
    """A simple commandline app for managing pointclouds in LAZ"""
    pass

@main.command()
@click.option('--file', required=True, help='File to convert to LAZ')
@click.option('--directoryTo', default=os.getcwd(), help='Directory to save LAZ')
def converttolaz(file, directoryto):
    """Convert a pointcloud from ['las', 'laz', 'e57', 'ply'] to LAZ and save it."""
    pointcloudMetadata = convertToLaz(file, directoryto)
    print(pointcloudMetadata)
    return pointcloudMetadata

@main.command()
@click.option('--lazFile', required=True, help='LAZ-file to convert')
@click.option('--directoryTo', default=os.getcwd(), help='Directory to save converted file')
@click.option('--convertTo', type=click.Choice(['las', 'laz', 'e57', 'ply'], case_sensitive=False))
def convertfromlaz(lazfile, directoryto, convertto):
    """Convert a LAZ-pointcloud to desired type."""
    pointcloudMetadata = convertFromLaz(lazfile, directoryto, convertto)
    print(pointcloudMetadata)
    return pointcloudMetadata

@main.command()
@click.option('--lazFile', required=True, help='LazFile to convert')
@click.option('--directoryTo', default=os.getcwd(), help='Directory to save')
@click.option('--untwinePath', default=os.getcwd(), help='Path to untwine')
def convertlaztoeptlaz(lazfile, directoryto, untwinepath):
    """Convert a pointcloud from LAZ to EPT-LAZ."""
    convertedLaz = convertLazToEPTLaz(lazfile, directoryto, untwinepath)
    print(convertedLaz)
    return convertedLaz


@main.command()
@click.option('--lazFile', required=True, help='LazFile to convert')
@click.option('--directoryTo', default=os.getcwd(), help='Directory to save')
def convertlazto2d(lazfile, directoryto):
    """Convert LAZ to a top rasterview in 2D."""
    metadata2D = convertLAZTo2D(lazfile, directoryto)
    print(metadata2D)
    return metadata2D

if __name__ == '__main__':
    main()
