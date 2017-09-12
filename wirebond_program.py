# Author: Steven Warren
# Contact: sbw986@gmail.com
# File name: Wirebonder_program.py
#
# Compatible Tool: K&S 8028

import csv
import operator
from xml.etree import ElementTree
from tkinter import *

# Define pads to bond
chip_pad_job = ['1C','2D','3A','15C','25D','32B']
package_pad_job = [3,14,27,29,35,42]

# Paths
import_dir = 'Import/'
export_dir = 'Export/'

# Files
#bga_file = 'fingers.wbt'
#chip_file = 'Bondpads.cif'
bga_file = 'BGA.csv'
chip_file = 'chip.csv'
wires_file = 'E2450C3B.WIR'

# Graphing Constants
scale_factor_BGA = 20
scale_factor_Chip = 20000
canvas_w = 1000
canvas_h = 800
pad_delta_BGA = 3
pad_delta_chip = 2

origin_x = canvas_w/2
origin_y = canvas_h/2

# Import BGA info from CSV file
bga_dict = {}
with open(import_dir + bga_file) as f:
   bga_reader = csv.reader(f)
   for row in bga_reader:
       finger_x = float(row[1])/scale_factor_BGA + origin_x
       finger_y = float(row[2])/scale_factor_BGA + origin_y
       bga_dict[row[0]] = [finger_x, finger_y]

# Import Chip info from CSV file
chip_dict = {}
chip_indices = {}
with open(import_dir + chip_file) as f:
    chip_reader = csv.reader(f)
    for row in chip_reader:
        chip_x = (float(row[2])/scale_factor_Chip + origin_x)
        chip_y = (float(row[3])/scale_factor_Chip + origin_x)
        chip_dict[row[0]] = [chip_x, chip_y]
        chip_indices[row[0]] = int(row[1])

# Generate Program Header
program_header = ''
with open(import_dir + wires_file) as template:
    for i in range(10):
        program_header += next(template)

# Generate Program
num_bonds = len(package_pad_job) * 2
wire_index = 1
left_str = ''
right_str = ''
for chip_pad,package_pad in zip(chip_pad_job,package_pad_job):
    if wire_index == 1:
        temp_str_left = 'connect' + '\t' + str(wire_index) + '\tL1\t\t' + str(package_pad) +'\t1\tSSB1_Loop'+ '\nto\t\tU1\t\t' + str(chip_indices[chip_pad + 'L']) + '\n\n'
    else:
        temp_str_left = 'connect' + '\t' + str(wire_index) + '\tL1\t\t' + str(package_pad) + '\nto\t\tU1\t\t' + str(chip_indices[chip_pad + 'L']) + '\n\n'
    temp_str_right = 'connect' + '\t' + str(num_bonds + 1 - wire_index) + '\tL1\t\t' + str(58*3 + 1 - package_pad) + '\nto\t\tU1\t\t' + str(chip_indices[chip_pad + 'R']) + '\n\n'
    left_str = left_str + temp_str_left
    right_str = temp_str_right + right_str
    wire_index +=1
program = program_header + left_str + right_str + 'end'
print(program)

# Export program
with open(export_dir + wires_file,'w') as export_file:
    export_file.write(program)
    export_file.close()

# Graphing Initialization
master = Tk()
w = Canvas(master,width = canvas_w, height = canvas_h)
w.pack()

# Draw Wirebonds
for chip_pad,package_pad in zip(chip_pad_job,package_pad_job):
    chip_pad_l = chip_pad + 'L'
    chip_pad_r = chip_pad + 'R'
    package_pad_l = str(package_pad)
    package_pad_r = str(58*3 + 1 - package_pad)
    w.create_line(chip_dict[chip_pad_l][0], chip_dict[chip_pad_l][1], bga_dict[package_pad_l][0], bga_dict[package_pad_l][1])
    w.create_line(chip_dict[chip_pad_r][0], chip_dict[chip_pad_r][1], bga_dict[package_pad_r][0], bga_dict[package_pad_r][1])

# Draw BGA
for p in bga_dict:
    x = bga_dict[p][0]
    y = bga_dict[p][1]
    w.create_rectangle(x - pad_delta_BGA, y - pad_delta_BGA, x + pad_delta_BGA, y + pad_delta_BGA)

# Draw Electrodes
for e in chip_dict:
    x = chip_dict[e][0]
    y = chip_dict[e][1]
    w.create_rectangle(x - pad_delta_chip, y - pad_delta_chip, x + pad_delta_chip, y + pad_delta_chip)

# Graph
mainloop()
