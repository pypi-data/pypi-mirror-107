# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['photorectify']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'lensfunpy>=1.8.0,<2.0.0',
 'numpy>=1.20.2,<2.0.0',
 'opencv-contrib-python>=4.5.1,<5.0.0',
 'scipy>=1.6.2,<2.0.0']

entry_points = \
{'console_scripts': ['photorectify = photorectify.__main__:main']}

setup_kwargs = {
    'name': 'photorectify',
    'version': '1.1.0',
    'description': 'Rectify lens distortions with Lensfun and OpenCV',
    'long_description': '# PhoToRectify\n\n**Notice:** Only tested for *Hasselblad L1D-20c* and *Pentax K-1 with HD Pentax-D FA 28-105mm f/3.5-5.6 ED DC WR.*\n\nUndistort images with the [Lensfun](https://lensfun.github.io/) library and [OpenCV](https://opencv.org/).\nMultiprocessing is supported to speed up the rectification.\n\n* Allowed input file formats: BMP, JPEG, JPEG 2000, PNG, PIF, SUN RASTERS, TIFF\n* Output file formats: JPEG, TIFF\n* Currently supported and used compressions:\n  + JPEG with Quality 97\n  + TIFF with JPEG-Compression\n* Custom meta data (optional arguments, use quotes if they contain spaces)\n\n## Installation\n\nInstallation into a virtual environment is recommended,\nbecause PhoToRectify depends on some other packages.\n\nInstall with: `pip install photorectify`  \nUpdate with: `pip install --upgrade photorectify`\n\n### Requirements\n\n* Python 3.7+\n* exiftool 10.38+ (older versions not tested; install it with your distribution’s package manager)\n* [PyExifTool](https://github.com/smarnach/pyexiftool) has been modified and is shipped with photorectify’s source code (removed `-n` optional argument for proper lens detection with Lensfun + added method `copy_tags()`)\n\n* For development: [poetry](https://python-poetry.org/) (do not skip the installation of the development dependencies!)\n\n## Alternative remapping method for undistort()\n\nInstead of using Pillow, you can also use OpenCV for remapping.\n```\nself.img_bgr_undist = lensfunpy.util.remap(\n    self.img_blob_bgr,\n    undistorted_coords)\n```\n\n## Examples\n\nRectify one photo in a directory (rectifed photo are stored in the same directory as the input file):  \n`photorectify Sampledata/DJI_0051.JPG`\n\nRectify all photos in a directory:  \n`photorectify Sampledata/`\n\nRectify into a custom output directory:  \n`photorectify Sampledata/ -o Sampledata/Rectified`\n\nAppend custom suffix to rectified photos (automatically adds an underscore):  \n`photorectify Sampledata/ -s rect`\n\nSpecify meta data if photo hasn’t any EXIF tags:\n```\nphotorectify Sampledata/DJI_0051.JPG \\\n    --model L1D-20c \\\n    --make Hasselblad \\\n    --FLength 10.26 \\\n    --FNumber 4.5\n```\n\nGet version:  \n`photorectify --version`\n\n## Development\n\nMore cameras and lenses can be supported by\nadding them to [`lensfun-db.xml`](https://gitlab.com/winkelband/photorectify/-/blob/master/src/photorectify/lensfun-db.xml).\nSee the [Lensfun database](https://github.com/lensfun/lensfun/tree/master/data/db).\n\nRunning tests:  \n`poetry run pytest -q tests/test_rectification.py`\n\n## Contribution\n\nTo help improving this python package,\nopen an issue or create a merge request.\n',
    'author': 'David Berthel',
    'author_email': 'code@davidberthel.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/archaeohelper/photorectify',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
