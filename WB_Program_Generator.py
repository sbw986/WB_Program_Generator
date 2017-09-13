# Author: Steven Warren
# Contact: sbw986@gmail.com
# File name: Wirebonder_program.py
#
# Compatible Tool: K&S 8028

import csv
from lines_intersect import lines_intersect
from cnt_spincast_expander import expand_bond_list
from tkinter import *

# Define pads to bond
chip_pad_job = ['2D','5C','10D','15A','16B','18C','20B','25A','30D']
package_pad_job = [4, 8, 9, 13, 22, 26, 27, 42, 35]

# Customize bond job for CNT work
chip_pad_job, package_pad_job = expand_bond_list(chip_pad_job, package_pad_job)

# Paths
import_dir = 'Import/'
export_dir = 'Export/'

# Files
bga_file = 'bga.csv'
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
        chip_y = (float(row[3])/scale_factor_Chip + origin_y)
        chip_dict[row[0]] = [chip_x, chip_y]
        chip_indices[row[0]] = int(row[1])

# Generate Program Header from .WIR template
program_header = ''
with open(import_dir + wires_file) as template:
    for i in range(10):
        program_header += next(template)

# Generate Program
num_bonds = len(package_pad_job) * 2
wire_index = 1
prog_str = ''
for chip_pad,package_pad in zip(chip_pad_job,package_pad_job):
    if wire_index == 1:
        temp_str = 'connect' + '\t' + str(wire_index) + '\tL1\t\t' + str(package_pad) +'\t1\tSSB1_Loop'+ '\nto\t\tU1\t\t' + str(chip_indices[chip_pad]) + '\n\n'
    else:
        temp_str = 'connect' + '\t' + str(wire_index) + '\tL1\t\t' + str(package_pad) + '\nto\t\tU1\t\t' + str(chip_indices[chip_pad]) + '\n\n'
    prog_str = prog_str + temp_str
    wire_index +=1
program = program_header + prog_str + 'end'

# Export program
with open(export_dir + wires_file,'w') as export_file:
    export_file.write(program)
    export_file.close()

# Graphing Initialization
master = Tk()
w = Canvas(master,width = canvas_w, height = canvas_h)
w.pack()

# Draw Wirebonds
drawn_bonds = []
for chip_pad,package_pad in zip(chip_pad_job,package_pad_job):
    i = w.create_line(chip_dict[chip_pad][0], chip_dict[chip_pad][1], bga_dict[str(package_pad)][0], bga_dict[str(package_pad)][1])
    for bond in drawn_bonds:
        if lines_intersect(w.coords(bond),w.coords(i)):
            w.itemconfig(bond, fill='red')
            w.itemconfig(i, fill='red')
    drawn_bonds.append(i)

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

