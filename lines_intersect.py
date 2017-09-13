# Author: Steven Warren
# Contact: sbw986@gmail.com
# File name: lines_intersect.py

import numpy as np

def lines_intersect(line1,line2):
    """
    Determines if lines intersect
    :param line1: list of X1, Y1, X2, Y2 floats defining line1
    :param line2: list X1, Y1, X2, Y2 floats defining line2
    :return: boolean, true if lines intersect, false otherwise
    """
    if line1 != line2:
        m1 = (line1[3]-line1[1])/(line1[2]-line1[0])
        b1 = line1[3] - m1*line1[2]
        m2 = (line2[3] - line2[1]) / (line2[2] - line2[0])
        b2 = line2[3] - m2*line2[2]
        x_int = (b2-b1)/(m1-m2)
        y_int = m1*x_int + b1

        min_x1 = np.min([line1[0], line1[2]])
        max_x1 = np.max([line1[0], line1[2]])
        min_y1 = np.min([line1[1], line1[3]])
        max_y1 = np.max([line1[1], line1[3]])
        min_x2 = np.min([line2[0], line2[2]])
        max_x2 = np.max([line2[0], line2[2]])
        min_y2 = np.min([line2[1], line2[3]])
        max_y2 = np.max([line2[1], line2[3]])

        if (x_int > min_x1 and x_int > min_x2 and x_int < max_x1 and x_int < max_x2 and
            y_int > min_y1 and y_int > min_y2 and y_int < max_y1 and y_int < max_y2):
            return True
        else:
            return False
    else:
        return True