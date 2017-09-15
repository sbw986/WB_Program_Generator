# WB Program Generator #

This function generates a program that can be used on a K&S 8028 wire bonder for automated bonding.  The function also
generates and saves a wire bonding diagram.

### DEPENDENCIES ###

Required: csv, tkinter, numpy, subprocess

Optional: xml.etree, operator - Needed for csv conversion scripts

### CONFIGURATION FILES ###

Users must provide three files in the 'Config' directory: package.csv, chip.csv, .WIR

* package.csv:

    * This file should be arranged into three columns: Finger #, Finger X Origin (um),
Finger Y Origin (um).

    * The 'xml_to_csv.py' script can be used to convert an APD generated xml output to the required
CSV formatting.

* chip.csv:

    * This file should be arranged into four columns: Pad ID value, Pad #, Pad X Origin (nm), Pad Y Origin (nm).

    * The 'cif_to_csv.py' script can be used to convert a CIF file to the required CSV format.

* .WIR:

    * Template .WIR file copied from K&S Bonder program.

### USAGE ###

* Ensure package.csv, chip.csv and a template .WIR file are saved in 'Config' folder.

* Create Job object:

    * Set file name values in object using object.config_files('package.csv','chip.csv',template'.WIR')

    * Define separate lists for chip pads to-be-bonded, package pads to-be-bonded, and wire groups.  Set values in object
respectively using object.define_wires(chip pads, package pads, wire groups)

    * Set object plotting parameters using object.plotting_parameters().  Default values are initialized.

* Run program by feeding Job object to generate_program function.

