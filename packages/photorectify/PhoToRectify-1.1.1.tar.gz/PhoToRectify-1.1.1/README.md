# PhoToRectify

**Notice:** Only tested for *Hasselblad L1D-20c* and *Pentax K-1 with HD Pentax-D FA 28-105mm f/3.5-5.6 ED DC WR.*

Undistort images with the [Lensfun](https://lensfun.github.io/) library and [OpenCV](https://opencv.org/).
Multiprocessing is supported to speed up the rectification.

* Allowed input file formats: BMP, JPEG, JPEG 2000, PNG, PIF, SUN RASTERS, TIFF
* Output file formats: JPEG, TIFF
* Currently supported and used compressions:
  + JPEG with Quality 97
  + TIFF with JPEG-Compression
* Custom meta data (optional arguments, use quotes if they contain spaces)

## Installation

Installation into a virtual environment is recommended,
because PhoToRectify depends on some other packages.

Install with: `pip install photorectify`  
Update with: `pip install --upgrade photorectify`

### Requirements

* Python 3.7+
* exiftool 10.38+ (older versions not tested; install it with your distribution’s package manager)
* [PyExifTool](https://github.com/smarnach/pyexiftool) has been modified and is shipped with photorectify’s source code (removed `-n` optional argument for proper lens detection with Lensfun + added method `copy_tags()`)

* For development: [poetry](https://python-poetry.org/) (do not skip the installation of the development dependencies!)

## Alternative remapping method for undistort()

Instead of using Pillow, you can also use OpenCV for remapping.
```
self.img_bgr_undist = lensfunpy.util.remap(
    self.img_blob_bgr,
    undistorted_coords)
```

## Examples

Rectify one photo in a directory (rectifed photo are stored in the same directory as the input file):  
`photorectify Sampledata/DJI_0051.JPG`

Rectify all photos in a directory:  
`photorectify Sampledata/`

Rectify into a custom output directory:  
`photorectify Sampledata/ -o Sampledata/Rectified`

Append custom suffix to rectified photos (automatically adds an underscore):  
`photorectify Sampledata/ -s rect`

Specify meta data if photo hasn’t any EXIF tags:
```
photorectify Sampledata/DJI_0051.JPG \
    --model L1D-20c \
    --make Hasselblad \
    --FLength 10.26 \
    --FNumber 4.5
```

Get version:  
`photorectify --version`

## Development

More cameras and lenses can be supported by
adding them to [`lensfun-db.xml`](https://gitlab.com/archaeohelper/photorectify/-/blob/master/src/photorectify/lensfun-db.xml).
See the [Lensfun database](https://github.com/lensfun/lensfun/tree/master/data/db).

Running tests:  
`poetry run pytest -q tests/test_rectification.py`

## Contribution

To help improving this python package,
open an issue or create a merge request.
