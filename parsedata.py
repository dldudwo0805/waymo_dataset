import tensorflow as tf
import math
import numpy as np
import itertools
import cv2
import glob
import argparse
tf.enable_eager_execution()
from waymo_open_dataset import dataset_pb2 as open_dataset
from data import *


def main(args):
	SAVE_CALIB_DATA = True
	FOLDERPATH = '/home/leeyj/Desktop/Parallels Shared Folders/Home/Downloads/waymo/'
	SAVEROOT = "/home/leeyj/Desktop/Data"
	FILEPATH = []
	CALIBRATION_FILENAME = "calib.csv"
	SAVE_CAMERA = True
	SAVE_LASER = False
	SHOW_IMAGE = True
	DELAY_TIME = 0
	FILENAME = None

	assert SAVE_LASER or SAVE_CAMERA or SHOW_IMAGE, "At least Save One Data or Show mode"

	for path in glob.glob(FOLDERPATH + "*.tfrecord"):
		FILEPATH.append(path)
	FILENAME = FILEPATH[0]
	dataset = tf.data.TFRecordDataset(FILENAME, compression_type='')

	frame_index = -1
	for data in dataset:
		frame_index += 1
		frame = open_dataset.Frame()
		frame.ParseFromString(bytearray(data.numpy()))
		if SAVE_CALIB_DATA is not False:
			calibration_file = open(CALIBRATION_FILENAME, 'w')
			calibration_file.write(FILENAME+'\n\n')
			if SAVE_CAMERA is True:
				for cali in frame.context.camera_calibrations:
					ret_val = parse_calibration_data(cali, "CAM")
					save_calibration_data(calibration_file, ret_val[0], ret_val[1], ret_val[2], ret_val[3])
			if SAVE_LASER is True:
				print("Todo")
			calibration_file.close()
			SAVE_CALIB_DATA = False
		if SAVE_CAMERA is True:
			for index, image in enumerate(frame.images):
				img = tf.image.decode_jpeg(image.image).numpy()
				save_image(SAVEROOT, open_dataset.CameraName.Name.Name(image.name), frame_index, img)
				if SHOW_IMAGE:
					img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
					cv2.imshow("test", img)
					key = cv2.waitKey(DELAY_TIME)
					if key == 27:
						exit(1)
					# push 'q' button
					elif key == 113:
						SHOW_IMAGE = False
						cv2.destroyAllWindows()
					elif key == 32:
						DELAY_TIME = 1

		if SAVE_LASER is True:
			print("TODO")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Converting Waymo Datset')
	main(parser.parse_args())
