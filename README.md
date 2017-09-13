# Wirebonder Automation #

This script generates a program that can be use on a K&S 8028 wirebonder for automated bonding.  The script also
generates a wirebond diagram.

### REQUIRED FILES ###

Users must provide two files in the 'Import' directory: BGA.csv and chip.csv

BGA.csv - This file should be arranged into three columns: Finger #, Finger X Origin (um),
Finger Y Origin (um).  The 'xml_to_csv.py' script can be used to convert an APD generated xml output to the required
CSV formatting.

chip.csv - This file should be arranged into four columns: Pad ID value, Pad #, Pad X Origin (nm), Pad Y Origin (nm).
The 'cif_to_csv.py' script can be used to convert as CIF file to the required CSV format.

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact