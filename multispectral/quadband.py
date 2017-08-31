####
# quadpreprocessing-proto.py
# Author: John Jackson
# Date: 05/22/2017
# Used for performing reflectance preprocessing for Quadband Imagery.
# Prototype script, not production ready.
####

import csv
import os
import sys
import numpy as np

from PIL import Image, ImageMath

PIX4DCSV_FILENAME = 'pix4d.csv'
NEWPIX4DCSV_FILENAME = 'newpix4d.csv'
AUTOEXPOSURECSV_FILENAME = 'autoexposure.csv'

# 655nm
# LEAKAGE_LIGHT_FACTOR = 0.05
# QE_FACTOR = 18.53

# 725nm
# LEAKAGE_LIGHT_FACTOR = 0.085
# QE_FACTOR = 46.57

# 800nm
LEAKAGE_LIGHT_FACTOR = 0.12
QE_FACTOR = 60.29

def post_process(dirs, processed_subdir='processed'):
	for dirstring in dirs:

		outdirstring = os.path.join(dirstring, processed_subdir)
		if not os.path.isdir(outdirstring): os.mkdir(outdirstring)
	
		csvname_autoexposure = os.path.join(dirstring, AUTOEXPOSURECSV_FILENAME)
		if not os.path.exists(csvname_autoexposure):
			raise Exception("File not found: " + csvname_autoexposure)
	
		csvname_pix4d = os.path.join(dirstring, PIX4DCSV_FILENAME)
		if not os.path.exists(csvname_pix4d):
			raise Exception("File not found: " + csvname_pix4d)

		csv_pix4d = open(csvname_pix4d, 'r')
		
		csvname_newpix4d = os.path.join(os.path.join(dirstring, processed_subdir), NEWPIX4DCSV_FILENAME)
		csv_newpix4d = open(csvname_newpix4d, 'w+')
		csv_newpix4d.write(csv_pix4d.readline())
		
		csvreader = csv.reader(csv_pix4d, delimiter=',')
		csvwriter = csv.writer(csv_newpix4d, delimiter=',')
		
		jpgfiles = []
	
		for row in csvreader:
			
			jpgfiles.append(row[0])
			
			row_new = row
			row_new[0] = row_new[0][0:len(row_new[0])-4] + '.tif'
			csvwriter.writerow(row_new)

		csv_pix4d.close()
		csv_newpix4d.close()
		
		# This is naiive, assuming the right order of jpg files and autoexposure measurements without checking the timestamp.
		csv_autoexposure = open(csvname_autoexposure, 'r')
		csv_autoexposure.readline()
		csvreader = csv.reader(csv_autoexposure, delimiter=',')

		# TODO: The value of this constant.
		k = 1.
		frame_period_us = 22000
		shutter_efficiency = 1/650

		# TODO: Graphical Progress Update
		for jpgfile, csvrow in zip(jpgfiles, csvreader):
		
			cal = 1./(k * int(csvrow[1]) * pow(2,int(csvrow[2])) * int(csvrow[3]))

			im = Image.open(os.path.join(dirstring,jpgfile))

			if im.mode == 'RGB':
				[_, img, _,] = im.split()
			elif im.mode == 'L':
				[img] = im.split()
			else:
				raise Exception("Invalid image format: " + im.mode)

			im.close()

			temp = ImageMath.eval("float(a)", a=img)
			nimg = np.asarray(temp, dtype=np.float32)

			# Apply Shutter Efficiency Correction
			shutter_efficiency_correction_factor = 1 / (1 + ((shutter_efficiency * frame_period_us) / int(csvrow[1])))
			nimg = nimg * shutter_efficiency_correction_factor

			# Apply Leakage Light Correction
			total = 0
			mean = nimg.mean()
			offset = LEAKAGE_LIGHT_FACTOR * mean
			nimg = nimg - offset


			# Apply Exposure Opportunity Correction
			nimg = nimg * cal

			# Apply Reflectance Scaling
			nimg = nimg * QE_FACTOR

			# Convert numpy to pillow
			out = Image.fromarray(nimg)
			
			outfile = os.path.join(outdirstring, jpgfile[0:len(jpgfile)-4] + '.tif')
			out.save(outfile, "TIFF")

		csv_autoexposure.close()
		
if __name__ == "__main__":
	usage = 'usage: quadband.py <list of dirs> <(opt) name of target subdirectory, default is \'processed\'>'
	if len(sys.argv) > 1:
		sys.argv.pop(0)
		post_process(sys.argv)
		
	else: 
		print(usage)