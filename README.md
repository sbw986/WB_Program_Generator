# WB Program Generator #

This script generates a program that can be use on a K&S 8028 wire bonder for automated bonding.  The script also
generates a wire bonding diagram.

### REQUIRED FILES ###

Users must provide three files in the 'Import' directory: bga.csv, chip.csv, [].WIR

bga.csv - This file should be arranged into three columns: Finger #, Finger X Origin (um),
Finger Y Origin (um).  The 'xml_to_csv.py' script can be used to convert an APD generated xml output to the required
CSV formatting.

chip.csv - This file should be arranged into four columns: Pad ID value, Pad #, Pad X Origin (nm), Pad Y Origin (nm).
The 'cif_to_csv.py' script can be used to convert a CIF file to the required CSV format.

[].WIR - Template .WIR file copied from any K&S Bonder program.

### RUNNING ###

Ensure bga.csv, chip.csv and a template .WIR file are saved in 'Import' folder

Within WB_Program_Generator:

* Define chip pads to-be-bonded in order using chip_pad_job and Pad ID value

* Define BGA pads to-be-bonded in order using package_pad_job and Finger #.  There should be a 1-1 correspondence to
chip_pad_job

* Define export file name using wires_file variable

Run WB_Program_Generator script

Change Graphing Constants within WB_Program_Generator script if plotting is not scaling properly


