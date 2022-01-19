# Import Ekahau Site Survey File in Cisco DNA-Center

Because it is not possible at this time to import Ekahau Site Survey Files in DNA-Center (only Ekahau Files in planning mode) i wrote this script 
to change the measured APs of a Site Survey File to Planned APs. After the conversion, the SiteSurvey File can be imported in DNA-Center.

# Howto:

1. Copy the files dnac_import_esx.py and antennaTypes.json in the directory where the .esx files are stored (all .esx files in the same folder will be converted). Copies of the .esx files will be made before making the conversion. So no changes where made to the original .esx files.

2. Execute the Python Script (there is no need to change anything in the .esx files)

3. After the script finished, an .esx file is created with the name <OriginalFilename.esx>_Import_DNA.esx. This file is for import in DNA-Center.

4. The building- and floor names (incl. the AP-Names in the floors) will also be extracted and written in the file DNA-Structure.log for every .esx file. This informations can be used to create the same hierarchy in DNA-Center and assign the right AP to the right floor.

5. Before you import the .esx file:
- make sure, that you have created the floors and building in DNA-Center with the same names as in the .esx file.
For that, you can use the DNA-Structure.log as overview.
- make sure, that the necessary APs are already assigned to the right floors.
- after import the APs are marked as "planned". When you click on the AP, you can map it to the right AP in DNA-Center.


It is still possible to open the created .esx files with ekahau, but because of file manipulation:
# DO NOT USE THE CREATED ESX-FILES FOR DATA ANALYTICS IN EKAHAU! THEY ARE JUST FOR IMPORT!
