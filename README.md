# ImageNormalization
Version 0.1

## What's Included
ImageNormalization includes scripts that normalize images from a Quadband sensor based on exposure time and the analog and digital gain sensors.

## Installation Instructions
These instructions have only been tested on a 64-bit Windows 10 machine in both Python 2.7 and 3.6 environments.
 and #### Package Installation
1. Inside of a terminal, `cd` to `ImageNormalization/`
2. Run `python steup.py install`

Now the `multispectral` package is available to use in Python.

##### Anaconda (Optional)
For more information on using Anaconda, the reader is encouraged to visit https://docs.continuum.io/anaconda/navigator/tutorials/manage-environments

1. Download and install Anaconda (Python 3.6 version recommended)
2. Launch Anaconda Navigator
2. Create a new Python 3.6 environment with a relevant name (e.g. "env-multispectral")

#### Dependencies

Currently the only dependancy of ImageNormalization is the `Pillow` image processing library. However, the image manipulation may be changed to use the `gdal` library in the future as other internal tools, such as those in `AnalysisTools`, use that for manipulation.

## Using MPP
Currently, there is only one script included with the ImageNormalization package. In order to work correctly, each image directory should contain the `pix4d.csv` and `autoexposure.csv` files.

### Command Line Tools
To calibrate one or more directories of images using the ImageNormalization command line tools, use:

`python <path-to-dir>/quadband.py <image-directory-1> <image-directory-2> ... <image-directory-N>`

### Python Functions
To use the ImageNormalization tools in a Python script, import the package using `import multispectral`. Each module is specified below.

* `quadband` module:
    * `post_process([list-of-image-directories], processed_subdir='processed')`
