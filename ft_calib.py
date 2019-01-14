from __future__ import print_function

import os
import numpy as np
from xml.dom import minidom

def load_calib_matrix(calib_file):

    try:
        xmldoc = minidom.parse(calib_file)
    except IOError:
        print("\nCalib File %s could not be found. Returning identity matrix...\n"%calib_file)
        return np.eye(6)

    itemlist = xmldoc.getElementsByTagName('UserAxis')

    mat = []
    for s in itemlist:

        parsed_mat = (s.attributes['values'].value).split()
        mat.append([float(i) for i in parsed_mat])

    calib_mat = np.asarray(mat)

    return calib_mat

def calibrate_ft_reading(ft_reading, calib_matrix):

	if ft_reading is None:
		return None

	return calib_matrix.dot(ft_reading) - np.array([2.5448695, 0.78797518, 3.17794361, -0.01304389, -0.35275512, -0.00642459]