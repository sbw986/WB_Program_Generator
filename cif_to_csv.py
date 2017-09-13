# Author: Steven Warren
# Contact: sbw986@gmail.com
# File name: cif_to_csv.py

import operator
from tkinter import *
import csv

# Converts CIF file of bondpads to formatted CSV file
def cif_to_csv(cif_file, export_name):
    """
    Generates a csv file given cif file input.  This function is tailored for CNT spin-cast patterns.
    :param cif_file: string defining cif file
    :param export_name: string defining name of CSV export file
    :return: none
    """

    # Paths
    import_dir = 'Import/'

    # Import Chip info from CIF file
    chip_x = []
    chip_y = []

    with open(import_dir + cif_file) as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == "P":
                text_re = re.sub('[,\nP;]',' ',line)
                split_txt = text_re.split(' ')[1:]
                split_txt_filt = list(filter(None, split_txt))
                float_vals = list(map(float,split_txt_filt))
                X_center = (float_vals[0]+float_vals[2])/2
                Y_center = (float_vals[1]+float_vals[5])/2*-1
                chip_x.append(X_center)
                chip_y.append(Y_center)

    chip_sorted = sorted(zip(chip_x, chip_y), key=operator.itemgetter(0, 1))

    chip_labels = [str(i+1)+'DL' for i in range(70)]
    chip_labels = chip_labels + ([str(i+1)+'CL' for i in range(70)])
    chip_labels = chip_labels + ([str(i+1)+'BL' for i in range(70)])
    chip_labels = chip_labels + ([str(i+2)+'AL' for i in range(69)])
    chip_labels = chip_labels + ([str(i+1)+'DR' for i in range(70)])
    chip_labels = chip_labels + ([str(i+1)+'CR' for i in range(70)])
    chip_labels = chip_labels + ([str(i+2)+'BR' for i in range(69)])
    chip_labels = chip_labels + ([str(i+2)+'AR' for i in range(69)])

    chip_dict = dict(zip(chip_labels,chip_sorted))
    chip_indices = range(1,len(chip_labels)+1)

    chip_list = []
    for i in range(len(chip_sorted)):
        chip_list.append([chip_labels[i],chip_indices[i],chip_sorted[i][0], chip_sorted[i][1]])

    with open(import_dir + export_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(chip_list)

if __name__ == '__main__':

    # Files
    cif_file = 'Bondpads.cif'
    export_name = 'chip.csv'

    # Run Conversion
    cif_to_csv(cif_file, export_name)