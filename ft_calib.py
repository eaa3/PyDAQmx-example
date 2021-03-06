from __future__ import print_function

import os
import numpy as np
from xml.dom import minidom

def load_calib_matrix(calib_file):

    try:
        xmldoc = minidom.parse(calib_file)
    except IOError:
        print("\nCalib File %s could not be found. Returning identity matrix...\n"%calib_file)
        return np.eye(6,dtype=np.float64)

    itemlist = xmldoc.getElementsByTagName('UserAxis')

    mat = []
    for s in itemlist:

        parsed_mat = (s.attributes['values'].value).split()
        mat.append([np.float64(i) for i in parsed_mat])

    calib_mat = np.asarray(mat,dtype=np.float64)

    return calib_mat

def calibrate_ft_reading(ft_reading, calib_matrix):

	if ft_reading is None:
		return None

	return calib_matrix.dot(ft_reading)