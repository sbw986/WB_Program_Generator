# Author: Steven Warren
# Contact: sbw986@gmail.com
# File name: WB_Program_Generator.py
#
# Compatible Tool: K&S 8028

import csv
import subprocess
from tkinter import *

from src.cnt_spincast_expander import *
from src.lines_intersect import lines_intersect

class Job:

    def __init__(self):
        pass

    def config_files(self,package_file, chip_file,wires_file):
        self.package_file = package_file
        self.chip_file = chip_file
        self.wires_file = wires_file

    def define_wires(self,chip_pad_job,package_pad_job,groups_job):
        self.chip_pad_job = chip_pad_job
        self.package_pad_job = package_pad_job
        self.groups_job = groups_job

    def plotting_parameters(self,scale_factor_package = 20, scale_factor_chip = 20000, canvas_w = 1000, canvas_h = 800,pad_delta_package = 3, pad_delta_chip = 2):
        self.scale_factor_package = scale_factor_package
        self.scale_factor_chip = scale_factor_chip
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.pad_delta_package = pad_delta_package
        self.pad_delta_chip = pad_delta_chip

def generate_program(Program_Info):

    # Paths
    import_dir = 'Config/'
    export_dir = 'Export/'

    # Define pads to bond
    chip_pad_job = Program_Info.chip_pad_job
    package_pad_job = Program_Info.package_pad_job
    groups_job = Program_Info.groups_job

    # Files
    package_file = Program_Info.package_file
    chip_file = Program_Info.chip_file
    wires_file = Program_Info.wires_file

    # Graphing Constants
    scale_factor_package = Program_Info.scale_factor_package
    scale_factor_chip = Program_Info.scale_factor_chip
    canvas_w = Program_Info.canvas_w
    canvas_h = Program_Info.canvas_h
    pad_delta_package = Program_Info.pad_delta_package
    pad_delta_chip = Program_Info.pad_delta_chip

    origin_x = canvas_w/2
    origin_y = canvas_h/2

    # Config BGA info from CSV file
    package_dict = {}
    with open(import_dir + package_file) as f:
       package_reader = csv.reader(f)
       for row in package_reader:
           finger_x = float(row[1])/scale_factor_package + origin_x
           finger_y = float(row[2])/scale_factor_package + origin_y
           package_dict[row[0]] = [finger_x, finger_y]

    # Config Chip info from CSV file
    chip_dict = {}
    chip_indices = {}
    with open(import_dir + chip_file) as f:
        chip_reader = csv.reader(f)
        for row in chip_reader:
            pad_x = (float(row[2])/scale_factor_chip + origin_x)
            pad_y = (float(row[3])/scale_factor_chip + origin_y)
            chip_dict[row[0]] = [pad_x, pad_y]
            chip_indices[row[0]] = int(row[1])

    # Generate Program Header from .WIR template
    program_header = ''
    with open(import_dir + wires_file) as template:
        stop_parse = False
        while stop_parse == False:
            program_header += next(template)
            if 'profile' in program_header:
                stop_parse = True
        program_header += next(template)
        program_header += next(template)

    # Generate Program
    wire_index = 1
    prog_str = ''
    for chip_pad,package_pad,group in zip(chip_pad_job,package_pad_job,groups_job):
        if wire_index == 1:
            temp_str = 'connect' + '\t' + str(wire_index) + '\tL1\t\t' + str(package_pad) + '\t' + str(group) + '\tSSB1_Loop'+ '\nto\t\tU1\t\t' + str(chip_indices[chip_pad]) + '\n\n'
        else:
            temp_str = 'connect' + '\t' + str(wire_index) + '\tL1\t\t' + str(package_pad) + '\t' + str(group) + '\nto\t\tU1\t\t' + str(chip_indices[chip_pad]) + '\n\n'
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
        i = w.create_line(chip_dict[chip_pad][0], chip_dict[chip_pad][1], package_dict[str(package_pad)][0], package_dict[str(package_pad)][1])
        for bond in drawn_bonds:
            if lines_intersect(w.coords(bond),w.coords(i)):
                w.itemconfig(bond, fill='red')
                w.itemconfig(i, fill='red')
        drawn_bonds.append(i)

    # Draw Package
    for p in package_dict:
        x = package_dict[p][0]
        y = package_dict[p][1]
        w.create_rectangle(x - pad_delta_package, y - pad_delta_package, x + pad_delta_package, y + pad_delta_package)

    # Draw Chip
    for c in chip_dict:
        x = chip_dict[c][0]
        y = chip_dict[c][1]
        w.create_rectangle(x - pad_delta_chip, y - pad_delta_chip, x + pad_delta_chip, y + pad_delta_chip)

    # Save Bonding Diagram
    w.update()
    w.postscript(file = 'tmp.ps',colormode = 'color')
    try:
        process = subprocess.call(["ps2pdf", "tmp.ps", "Export/Diagram.pdf"])
        process = subprocess.call(["rm", "tmp.ps"])
    except:
        print('Problem Exporting Bonding Diagram')

    # Graph
    mainloop()

if __name__ == '__main__':


    #Job 1
    chip_pad_job = ['4B', '4D', '6A', '6D', '9C',
                    '10A', '12D', '13B', '14B', '15B',
                    '21A', '21B', '23B', '24C', '31C',
                    '36B', '38C', '46A', '46C', '51C',
                    '53A', '57D', '59A', '61C', '66C']
    #chip_pad_job = chip_pad_job.split(' ')

    package_pad_job = [5, 7, 9, 11, 13,
                       15, 17, 19, 21, 23,
                       25, 27, 29, 31, 33,
                       35, 37, 39, 41, 43,
                       45, 47, 49, 51, 53]


    #package_pad_job = list(map(int,package_pad_job.split(' ')))

    if len(chip_pad_job) != len(package_pad_job):
        print('PROBLEM')
    if max(package_pad_job) > 58:
        print('PROBLEM')

    groups_job = []

    chip_pad_job, package_pad_job, groups_job = expand_bond_list_cnf(chip_pad_job, package_pad_job)

    job_sbw = Job()
    job_sbw.config_files('package.csv','chip.csv','IE739303.WIR')
    job_sbw.define_wires(chip_pad_job, package_pad_job, groups_job)
    job_sbw.plotting_parameters()

    generate_program(job_sbw)


    """
    #Job 2
    chip_pad_job = ['8','10','11','17','24','25']
    package_pad_job = [3,8,13,18,23,28]
    groups_job = []

    chip_pad_job, package_pad_job, groups_job = expand_bond_list_erik(chip_pad_job, package_pad_job)

    job_erik = Job()
    job_erik.config_files('package.csv','chip_erik.csv','II73A500.WIR')
    job_erik.define_wires(chip_pad_job, package_pad_job, groups_job)
    job_erik.plotting_parameters()

    generate_program(job_erik)
    """


    """
    # Job 3
    chip_pad_job = ['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15','C16',
                    'D1', 'D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14','D15','D16']
    package_pad_job = [22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,
                       38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]
    groups_job = []

    chip_pad_job, package_pad_job, groups_job = expand_bond_list_gonzalez(chip_pad_job, package_pad_job)

    job_gonzalez = Job()
    job_gonzalez.config_files('package.csv', 'chip_gonzalez.csv', 'IS72CA21.WIR')
    job_gonzalez.define_wires(chip_pad_job, package_pad_job, groups_job)
    job_gonzalez.plotting_parameters()

    generate_program(job_gonzalez)
    """
