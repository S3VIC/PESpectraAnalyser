import numpy as np
import os
import src.params.parameters as par


def derivative(x_coord, y_coord):
    return np.diff(y_coord) / np.diff(x_coord)


def get_file_names(path):
    file_list = []
    for filename in os.listdir(path):
        # -3 parameter to separate extension from the filename
        if filename[-3:].upper() == par.FILENAME_EXTENSION:
            temp_file = os.path.join(path, filename)
            if os.path.isfile(temp_file):
                file_list.append(filename)
    return file_list
