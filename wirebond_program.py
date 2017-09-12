# Steven Warren
# Wirebonder program
# K&S 8028

import operator
from xml.etree import ElementTree
from tkinter import *
from shutil import copyfile

# Define pads to bond
chip_pad_job = ['1C','2D','3A']
package_pad_job = [3,10,27]

# Paths
bga_file = 'fingers.wbt'
chip_file = 'Bondpads.cif'
import_file = 'E2450C3B.WIR'

# Graphing Constants
scale_factor_BGA = 20
scale_factor_Chip = 20000
canvas_w = 1000
canvas_h = 800
pad_delta_BGA = 3
pad_delta_chip = 2

# Import BGA info from APD xml file
with open(bga_file) as f:
    tree = ElementTree.parse(f)

bga_dict = {}
origin_x = canvas_w/2
origin_y = canvas_h/2
for child in tree.findall('finger'):
    finger_x = child.find('loc_x').text
    finger_x = float(finger_x.split(' ')[0])
    finger_x = finger_x/scale_factor_BGA + origin_x

    finger_y = child.find('loc_y').text
    finger_y = float(finger_y.split(' ')[0])*-1
    finger_y = finger_y/scale_factor_BGA + origin_y

    label_str = child.find('label').text
    label_val = int(re.sub('[BF]', '', label_str))

    bga_dict[str(label_val)] = [finger_x, finger_y]

# Import Chip info from CIF file
chip_x = []
chip_y = []
with open(chip_file) as f:
    lines = f.readlines()
    for line in lines:
        if line[0] == "P":
            text_re = re.sub('[,\nP;]',' ',line)
            split_txt = text_re.split(' ')[1:]
            split_txt_filt = list(filter(None, split_txt)) 
            float_vals = list(map(float,split_txt_filt))
            X_center = (float_vals[0]+float_vals[2])/2
            Y_center = (float_vals[1]+float_vals[5])/2*-1
            chip_x.append(X_center/scale_factor_Chip + origin_x)
            chip_y.append(Y_center/scale_factor_Chip + origin_y)

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
chip_indices = dict(zip(chip_labels,range(1,len(chip_labels)+1)))

# Generate Program Header
program_header = ''
with open(import_file) as template:
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
copyfile(import_file,import_file + '.backup')
with open(import_file,'w') as export_file:
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
