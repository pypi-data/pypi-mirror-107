#!/usr/bin/env python

'''PhoToRectify

Module for recitifying photos
with Lensfun and OpenCV.

Does multiprocessing.

Param:
    path: Path to image
    lensfun_xml: Path to Lenfun Database (format: XML)
    outdir: Path to output directory (can be None → same as input dir)
    suffix: String for appended suffix of exported file
'''


import argparse as ap
import imghdr
import multiprocessing as mp
import pathlib
import os
import sys

import cv2
import lensfunpy
import lensfunpy.util
import numpy as np
import PIL
import PIL.Image
import PIL.ExifTags

from . import __version__
from photorectify import exiftool


'''
TODO: Define Exception Classes, so errors from ImageRectification() can be fetched
      inside rectify() where the correspondening filename can be added, but the name
      should not be raised inside ImageRectification() (so self.file_in can safely be deleted!). Module should be sufficent when only using with one file or import into other python script (so maybe try blocks should go to main()?).
      → Define classes.
      → Refactor rectify() with try blocks.
      → Remove self.file_in.
'''

# Constants, which can be overwritten by argparse.
LENSFUN_DB = pathlib.Path(__file__).parent.joinpath('lensfun-db.xml').resolve()
TIFF_COMPRESS = 'jpeg'
JPEG_QUALITY = 97


def open_lensfun(lensfun_xml):
    '''Open Lensfun database.
    '''
    try:
        with open(lensfun_xml, 'r') as file:
            xml = file.read()
        lensfun_db = lensfunpy.Database(xml=xml)
    except lensfunpy._lensfun.XMLFormatError:
        print('TypeError: Not a correct XML file. See provided lensfun-db.xml as an example.')
        sys.exit(1)

    return lensfun_db


class ImageMeta():
    '''Return EXIF data and px dimensions.
    If no EXIF tags are present, let user
    specify meta data as arguments.
    '''
    def __init__(self, filename, meta_user):
        '''
        param: image = path filename
        '''

        self.image = filename
        self.meta_user = meta_user

    def get_exif_tags(self, image, tag_names):
        '''Return tags which names
        were specified.

        param: image: path as str
        param: tag_names: list of tags to return
        '''

        with exiftool.ExifTool() as et:
            return et.get_tags(tag_names, image)

    def cam_params(self):
        '''Return camera parameters (tags).
        Overwrite EXIF tags if manually
        specified by user.
        '''

        distortion_tags = ['EXIF:Make', 'EXIF:Model', 'Composite:LensID',
                          'EXIF:FNumber#', 'EXIF:FocalLength#',]
        tags = self.get_exif_tags(str(self.image), distortion_tags)

        # Overwrite tags.
        if self.meta_user['EXIF:Make']:
            tags['EXIF:Make'] = self.meta_user['EXIF:Make']
        if self.meta_user['EXIF:Model']:
            tags['EXIF:Model'] = self.meta_user['EXIF:Model']
        if self.meta_user['Composite:LensID']:
            tags['Composite:LensID'] = self.meta_user['Composite:LensID']
        if self.meta_user['EXIF:FocalLength']:
            tags['EXIF:FocalLength'] = self.meta_user['EXIF:FocalLength']
        if self.meta_user['EXIF:FNumber']:
            tags['EXIF:FNumber'] = self.meta_user['EXIF:FNumber']

        return tags


class ImageRectification():
    '''Rectify image and
    save as JPG or TIF.
    '''

    def __init__(self,
                 lensfun_db,
                 make, model, lens,
                 width, heigth, foclen, fnumber,
                 img_blob_bgr, file_in):
        self.db = lensfun_db
        self.make = make
        self.model = model
        self.lens = lens
        self.width = width
        self.heigth = heigth
        self.foclen = foclen
        self.fnumber = fnumber
        self.img_blob_bgr = img_blob_bgr
        self.file_in = file_in # Only for IndexError, useful when using multiprocessing files. See Todo.

    def find_cam_meta_lensfun(self):
        try:
            cam = self.db.find_cameras(self.make, self.model,
                                          loose_search=False)[0]
            #print(cam) # For --verbose and DEBUG only.
        except IndexError:
            print(f'**{self.file_in.name}**: CameraNotFoundInLensfunError: {self.make} {self.model}')
            sys.exit(1)
        try:
            lens = self.db.find_lenses(cam, None, self.lens,
                                            loose_search=True)[0]
            #print(lens) # For --verbose and DEBUG only.
        except IndexError:
            print(f'**{self.file_in.name}**: LensNotFoundInLensfunError: {self.lens}')
            sys.exit(1)

        return cam, lens

    def undistort(self):
        # Get modifier.
        cam, lens = self.find_cam_meta_lensfun()
        mod = lensfunpy.Modifier(
            lens,
            cam.crop_factor,
            self.width, self.heigth)
        mod.initialize(self.foclen, self.fnumber)

        # Remap with undistorted coordinates from modifier.
        undist_coords = mod.apply_geometry_distortion()
        self.img_undist_bgr = cv2.remap(
            self.img_blob_bgr,
            undist_coords,
            None,
            cv2.INTER_LANCZOS4
            )

        return self

    def convert_colorspace(self, image, conv_code):
        '''Transform OpenCV image color
        if output for PIL Image.

        Param:
            conv_code: cv2.COLOR_BGR2RG: BGR into PIL Image RGB.
        '''

        return cv2.cvtColor(image, conv_code)

    def save_pil(self, file_out):
        '''Save image as file with PIL.
        '''
        conv_code = cv2.COLOR_BGR2RGB
        img_rgb = self.convert_colorspace(self.img_undist_bgr, conv_code)

        with PIL.Image.fromarray(img_rgb) as image:
            if file_out.suffix == '.tif':
                alpha = PIL.Image.new('L', (self.width, self.heigth),
                                      color=255)
                image.putalpha(alpha)
                image.save(str(file_out), format='TIFF', compression=TIFF_COMPRESS)
            elif file_out.suffix == '.jpg':
                image.save(str(file_out), format='JPEG', quality=JPEG_QUALITY)
            else:
                print('KeyError: Filetype not supported! Use .jpg or .tif.')

    def save_cv2(self, file_out):
        '''Save image as file with OpenCV.
        '''
        # TODO: Use cv2.imwrite instead of PIL.Image.fromarray().
        # * problem: TIFF COMPRESSION (=JPEG does not work;
        #   LZW results in quite large file size)
        # * problem: ALPHA/4th CHANNEL = "undefined" in gdalinfo and QGIS
        # * info: libtiff uses int values for compression method (0, 1, 5, 7 etc.)
        if file_out.suffix == '.tif':
            img_bgra = cv2.cvtColor(self.img_undist_bgr, cv2.COLOR_BGR2BGRA)
            img_bgra[...,3] = 255
            # Get channels of image.
            #b_channel, g_channel, r_channel = cv2.split(self.img_undist_bgr)
            ## Create a dummy alpha channel image.
            #alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
            #alpha_channel = alpha_channel.astype(np.uint8)
            # First create the image with alpha channel
            # Then assign the mask to the last channel of the image
            #img_rgba[:, :, 3] = alpha_channel
            #img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
            #params = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            cv2.imwrite(str(file_out), img_bgra,
                        [cv2.IMWRITE_TIFF_COMPRESSION, 5])
        elif file_out.suffix == '.jpg':
            # params = 
            cv2.imwrite(str(file_out), self.img_undist_bgr,
                        [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
        else:
            print('KeyError: Filetype not supported! Use .jpg or .tif.')

    def write_exif(self, from_filename, to_filename):
        '''Write original EXIF tags if available.
        '''
        with exiftool.ExifTool() as et:
            et.copy_tags(bytes(from_filename), bytes(to_filename))


def is_image(file):
    '''Return True if file is a valid image.
    '''
    return imghdr.what(file) != None


def main():
    parser = ap.ArgumentParser(description='Rectify lens distortions with Lensfun')
    parser.add_argument('Path',
        metavar='path',
        type=pathlib.Path,
        help='specify a photo or a directory to process')
    parser.add_argument('--recursively', '-r',
        action='store_true',
        help='looking recursively for photos')
    parser.add_argument('--outdir', '-o',
        action='store',
        type=pathlib.Path,
        nargs='?',
        help='specify an output directory')
    parser.add_argument('--suffix', '-s',
        action='store',
        type=str,
        nargs='?',
        default='ve',
        help='specify a suffix to append to basename (default: "ve")')
    parser.add_argument('--jpg', '-j',
        action='store_true',
        help='export as JPEG (default: TIFF with alpha channel); using a lowercase file suffix')
    # for saving with openCV: JPEG_QUALITY range1-100, int; TIFF_COMPRESS: LZW etc. see libtiff
    parser.add_argument('--noExif', '-n',
        action='store_false',
        help='copy tags from input photo to output photo (default: True)')
    parser.add_argument('--lensfun', '-l',
        metavar='path',
        type=pathlib.Path,
        default=LENSFUN_DB,
        help='specify an alternative lensfun database (format: XML)')
    parser.add_argument('--Make',
        type=str,
        help='specify a make')
    parser.add_argument('--Model',
        type=str,
        help='specify a model')
    parser.add_argument('--LensID',
        type=str,
        help='specify a LensID (see exiftool for help)')
    parser.add_argument('--FLength',
        type=float,
        help='specify the focal length (decimal)')
    parser.add_argument('--FNumber',
        type=float,
        help='specify the focal ratio (f-stop) (decimal)')
    parser.add_argument('--version',
		action='version',
		version="%(prog)s (version {version})".format(version=__version__))
    p_args = parser.parse_args()

    path = p_args.Path
    lensfun_xml = p_args.lensfun
    outdir = p_args.outdir
    suffix = p_args.suffix
    preserve_exif = p_args.noExif
    meta_user = {
        'EXIF:Make': p_args.Make,
        'EXIF:Model': p_args.Model,
        'Composite:LensID': p_args.LensID,
        'EXIF:FocalLength': p_args.FLength,
        'EXIF:FNumber': p_args.FNumber,
        }

    photos = []
    if path.is_file():
        if is_image(path):
            photos.append(path)
    elif path.is_dir():
        if p_args.recursively:
            for file in path.rglob(r'**/*'):
                if is_image(file):
                    photos.append(file)
        else:
            for file in path.glob(r'*'):
                if is_image(file):
                    photos.append(file)
    if not photos:
        print("FileError: No valid image file")
        sys.exit(1)

    # Load lensfun_db once.
    lensfun_db = open_lensfun(lensfun_xml)

    # Start recitification processes.
    jobs = []
    for photo in photos:
        proc = mp.Process(target=rectify, args=(
            lensfun_db, photo.resolve(), meta_user, p_args, preserve_exif, outdir, suffix
            )
        )
        jobs.append(proc)
        proc.start()


def rectify(lensfun_db, file_in, meta_user, p_args, preserve_exif, outdir, suffix):
    # Get meta data from image.
    image = ImageMeta(file_in, meta_user)
    meta = image.cam_params()
    try:
        meta['EXIF:Make']
        meta['EXIF:Model']
        meta['EXIF:FocalLength']
        meta['EXIF:FNumber']
        meta['Composite:LensID']
    except KeyError as err:
        if str(err) in [
                "'EXIF:Make'", "'EXIF:Model'", 
                "'EXIF:FocalLength'", "'EXIF:FNumber'"]:
            print(f'''**{file_in.name}**: '''
                  f'''KeyError: {err}. '''
                  f'''You can specify tags as optional arguments. See --help.''')
            sys.exit(1)
        elif str(err) == "'Composite:LensID'":
            # Assume fixed lens.
            print(f'''**{file_in.name}**: '''
                  f'''Warning: No LensID in EXIF found. '''
                  f'''Assuming fixed lens. '''
                  f'''Will try to find a match with camera model in Lensfun DB.''')
            meta['Composite:LensID'] = meta['EXIF:Model']

    # Load image for OpenCV.
    img_blob_bgr = cv2.imread(str(file_in))
    # Add width, height.
    meta['Width'] = img_blob_bgr.shape[1]
    meta['Height'] = img_blob_bgr.shape[0]
    #print(f'{file_in.name}: {str(meta).strip("{}")}') # For --verbose and DEBUG only.

    # Rectify image with Lensfun and OpenCV.
    img_rect = ImageRectification(
        lensfun_db = lensfun_db,
        make = meta['EXIF:Make'],
        model = meta['EXIF:Model'],
        lens = meta['Composite:LensID'],
        width = meta['Width'],
        heigth = meta['Height'],
        foclen = meta['EXIF:FocalLength'],
        fnumber = meta['EXIF:FNumber'],
        img_blob_bgr = img_blob_bgr,
        file_in = file_in
        )

    if p_args.jpg:
        filename = f'{file_in.stem}_{suffix}.jpg'
    else:
        filename = f'{file_in.stem}_{suffix}.tif'
    if outdir:
        file_out = outdir.joinpath(filename).resolve()
    else:
        file_out = file_in.parent.joinpath(filename).resolve()
    pathlib.Path(file_out.parent).mkdir(parents=True, exist_ok=True)

    img_rect.undistort()
    img_rect.save_pil(file_out)
    if preserve_exif:
        img_rect.write_exif(file_in, file_out)
    print(f'{file_in.name} → {file_out}')


if __name__ == '__main__':

    main()
