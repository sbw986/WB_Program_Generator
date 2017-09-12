from xml.etree import ElementTree
import csv
from tkinter import *

# Converts XML file of fingers generated from APD
# to formatted CSV file
def xml_to_csv(apd_file, export_name):

    # Paths
    import_dir = 'Import/'
    export_dir = 'Import/'

    # Import BGA info from APD xml file
    with open(import_dir + apd_file) as f:
        tree = ElementTree.parse(f)

    bga_list = []

    for child in tree.findall('finger'):
        finger_x = child.find('loc_x').text
        finger_x = float(finger_x.split(' ')[0])

        finger_y = child.find('loc_y').text
        finger_y = float(finger_y.split(' ')[0])*-1

        label_str = child.find('label').text
        label_val = int(re.sub('[BF]', '', label_str))

        bga_list.append([label_val,finger_x,finger_y])

    with open(import_dir + export_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(bga_list)

if __name__ == '__main__':

    # Files
    apd_file = 'fingers.wbt'
    export_name = 'BGA.csv'

    # Run Conversion
    xml_to_csv(apd_file, export_name)



