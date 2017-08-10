"""
double4k.py.py

@author: John Jackson
@date: 08/10/2017

Used for performing reflectance preprocessing for Double4k Imagery.
Prototype script, not production ready.
"""

import csv
import os
import sys

import piexif
from PIL import Image, ImageMath

PIX4DCSV_FILENAME = 'pix4d.csv'
NEWPIX4DCSV_FILENAME = 'newpix4d.csv'
AUTOEXPOSURECSV_FILENAME = 'autoexposure.csv'


def post_process(dirs, processed_subdir='processed'):
	for dirstring in dirs:

		outdirstring = os.path.join(dirstring, processed_subdir)
		if not os.path.isdir(outdirstring): os.mkdir(outdirstring)

		# csvname_autoexposure = os.path.join(dirstring, AUTOEXPOSURECSV_FILENAME)
		# if not os.path.exists(csvname_autoexposure):
		# 	raise Exception("File not found: " + csvname_autoexposure)
		#
		# csvname_pix4d = os.path.join(dirstring, PIX4DCSV_FILENAME)
		# if not os.path.exists(csvname_pix4d):
		# 	raise Exception("File not found: " + csvname_pix4d)

		# csv_pix4d = open(csvname_pix4d, 'r')
		#
		# csvname_newpix4d = os.path.join(os.path.join(dirstring, processed_subdir), NEWPIX4DCSV_FILENAME)
		# csv_newpix4d = open(csvname_newpix4d, 'w+')
		# csv_newpix4d.write(csv_pix4d.readline())
		#
		# csvreader = csv.reader(csv_pix4d, delimiter=',')
		# csvwriter = csv.writer(csv_newpix4d, delimiter=',')

		allfiles = os.listdir(dirstring)
		jpgfilenames = [name for name in allfiles if str.find(name, '.jpg') > 0]

		# for row in csvreader:
		# 	jpgfiles.append(row[0])
		#
		# 	row_new = row
		# 	row_new[0] = row_new[0][0:len(row_new[0]) - 4] + '.tif'
		# 	csvwriter.writerow(row_new)
		#
		# csv_pix4d.close()
		# csv_newpix4d.close()

		# This is naiive, assuming the right order of jpg files and autoexposure measurements without checking the timestamp.
		# csv_autoexposure = open(csvname_autoexposure, 'r')
		# csv_autoexposure.readline()
		# csvreader = csv.reader(csv_autoexposure, delimiter=',')

		# TODO: The value of this constant.
		k = 1.

		# TODO: Graphical Progress Update
		for jpgfile in jpgfilenames:

			jpgfilename = os.path.join(dirstring, jpgfile)
			exif_dict = piexif.load(jpgfilename)

			exposure_tup = exif_dict['Exif'][33434]
			exposure_time = exposure_tup[0]/exposure_tup[1]
			print("Exposure time: " + str(exposure_time))

			# f_tup = exif_dict['Exif'][33437]
			# f_number = f_tup[0]/f_tup[1]

			iso = exif_dict['Exif'][34855]
			iso_factor = iso/100
			print("ISO factor: " + str(iso_factor))

			# brightness = exif_dict['Exif'][37379]
			# meteringmode = exif_dict['Exif'][37383]
			# focallength = exif_dict['Exif'][37386]

			cal = 1. / (k * exposure_time * iso_factor)

			im = Image.open(os.path.join(dirstring, jpgfile))
			[red, green, blue, ] = im.split()
			im.close()

			# Red
			temp = ImageMath.eval("float(a)", a=red)
			out = temp.point(lambda i: i * cal)
			outsubdirstring = os.path.join(outdirstring, 'red')
			if not os.path.isdir(outsubdirstring): os.mkdir(outsubdirstring)
			outfile = os.path.join(outsubdirstring, jpgfile[0:len(jpgfile) - 4] + '-red.tif')
			out.save(outfile, "TIFF")

			# Red
			temp = ImageMath.eval("float(a)", a=green)
			out = temp.point(lambda i: i * cal)
			outsubdirstring = os.path.join(outdirstring, 'green')
			if not os.path.isdir(outsubdirstring): os.mkdir(outsubdirstring)
			outfile = os.path.join(outsubdirstring, jpgfile[0:len(jpgfile) - 4] + '-green.tif')
			out.save(outfile, "TIFF")

			# Red
			temp = ImageMath.eval("float(a)", a=blue)
			out = temp.point(lambda i: i * cal)
			outsubdirstring = os.path.join(outdirstring, 'blue')
			if not os.path.isdir(outsubdirstring): os.mkdir(outsubdirstring)
			outfile = os.path.join(outsubdirstring, jpgfile[0:len(jpgfile) - 4] + '-blue.tif')
			out.save(outfile, "TIFF")

		#csv_autoexposure.close()


if __name__ == "__main__":
	usage = 'usage: double4k.py <list of dirs> <(opt) name of target subdirectory, default is \'processed\'>'
	if len(sys.argv) > 1:
		sys.argv.pop(0)
		post_process(sys.argv)

	else:
		print(usage)