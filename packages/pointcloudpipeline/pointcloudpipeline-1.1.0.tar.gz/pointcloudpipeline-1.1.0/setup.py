from setuptools import setup, find_packages

VERSION = '1.1.0'
DESCRIPTION = 'A simple commandline app for converting pointclouds and get 2D images out of a pointclouds.'
LONG_DESCRIPTION = 'A simple commandline app for converting pointclouds. You can convert your Pointcloud into a viewable Entwine format or in a 2D raster.'

setup (
    name = 'pointcloudpipeline',
    version = VERSION,
    author = 'Nadine Sennhauser and Denis Nauli',
    author_email = 'nadine.sennhauser@ost.ch',
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages = find_packages(),
    install_requires = [
        'click',
        'numpy',
        'cython',
        'packaging',
        'scikit-build',
        'pdal'
    ],
    keywords = ['pointcloud','convert','pointcloudbrowser'],
    python_requires = '>=3.1',
    scripts=['pointcloudpipeline/pipeline_worker.py'],
    entry_points='''
        [console_scripts]
        pointcloudpipeline=pointcloudpipeline.__main__:main
    ''',
    license='BSD-3',
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
