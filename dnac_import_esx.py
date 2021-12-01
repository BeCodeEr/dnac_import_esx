import zipfile
import glob
import shutil
import json
import os

if not os.path.isfile(r"./antennaTypes.json"):
   print("ERROR: 'antennaTypes.json' not present in the directory! Operation aborted!")
   exit()
#Delete privious created esx-Files
files = glob.glob('*Import_DNA.esx')
for file in files:
    os.remove(file)
if os.path.isfile("DNA-Structure.log"):
  os.remove("DNA-Structure.log")
DNA_Structure_File = open("DNA-Structure.log","a")
DNA_Structure_File.write('The following Building/Floor structure is defined in Ekahau-File.\nCreate the same structure in DNA-Center.\nIf a building is defined, you have to import the file in DNA-C at the Area-Level. \nIf no building is defined, you have to import the file in DNA-C at the Building-Level.')
DNA_Structure_File.write('\n---------------------------------------------\n')  
#List of all *.esx Files in the directory
list_esx = glob.glob(r"*.esx")

if not list_esx:
    print('No .esx Files found in the directory! /n Operation aborted!')
    exit()

#For-loop for all entries in list_esx (For all esx Files)
x=0
for i in list_esx:
    print('Processing File: ' , list_esx[x])
    #Make copy of original files
    source = "./" + list_esx[x]
    destination = "./" + list_esx[x] + '_Import_DNA.esx'
    shutil.copyfile(source, destination)        
    
    #Extract .esx File to temporary directory
    myesx = zipfile.ZipFile(destination) 
    myExtractfolder = destination[:-4]
    myesx.extractall(myExtractfolder)
    myesx.close
    #To convert the APs in simulated APs, we need to create a file 
     #Top of file we need to create
    with open('simulatedRadios.json', 'a') as f:
        StartOfSimFile="""{
  "simulatedRadios": ["""
        f.write(StartOfSimFile)
        f.close
    
    #Open accessPoints.json to readout the AP-IDs
    with open('./' + myExtractfolder + '/accessPoints.json') as json_file:
        data = json.load(json_file)    
    #create entry for each AP in accessPoints.json
    RadioFile = ''
    for a in data['accessPoints']:
        ap_id = a['id']
        ap_name = a['name']
        #print('AP-NAME: ' + ap_name + ' || AP-ID : ' + ap_id )
        RadioFile = RadioFile + """
    {
      "accessPointId": """ + '"' + ap_id + '"' + """,
      "accessPointIndex": 1,
      "transmitPower": 13.979400086720377,
      "channel": [
        36
      ],
      "antennaTypeId": "d408bff9-4379-4c37-b836-7dc4401c82dc",
      "antennaDirection": 0.0,
      "antennaTilt": 0.0,
      "antennaHeight": 2.4,
      "antennaMounting": "CEILING",
      "technology": "AC",
      "radioTechnology": "IEEE802_11",
      "spatialStreamCount": 1,
      "shortGuardInterval": false,
      "greenfield": false,
      "defaultAntennas": [
        {
          "radioTechnology": "IEEE802_11",
          "frequencyBand": "TWO",
          "antennaTypeId": "553bf358-3cd4-474b-a1c1-d264ce747173"
        },
        {
          "radioTechnology": "IEEE802_11",
          "frequencyBand": "FIVE",
          "antennaTypeId": "d408bff9-4379-4c37-b836-7dc4401c82dc"
        }
      ],
      "enabled": true,
      "id": "188e59e0-24b1-42e1-aa5f-8e433a5dcc8d",
      "status": "CREATED"
    },
    {
      "accessPointId": """ + '"' + ap_id + '"' + """,
      "accessPointIndex": 0,
      "transmitPower": 8.000293592441343,
      "channel": [
        1
      ],
      "antennaTypeId": "553bf358-3cd4-474b-a1c1-d264ce747173",
      "antennaDirection": 0.0,
      "antennaTilt": 0.0,
      "antennaHeight": 2.4,
      "antennaMounting": "CEILING",
      "technology": "N",
      "radioTechnology": "IEEE802_11",
      "spatialStreamCount": 1,
      "shortGuardInterval": false,
      "greenfield": false,
      "defaultAntennas": [
        {
          "radioTechnology": "IEEE802_11",
          "frequencyBand": "TWO",
          "antennaTypeId": "553bf358-3cd4-474b-a1c1-d264ce747173"
        },
        {
          "radioTechnology": "IEEE802_11",
          "frequencyBand": "FIVE",
          "antennaTypeId": "52768c36-4aea-4e23-adf8-c975d9a29732"
        }
      ],
      "enabled": true,
      "id": "c1ba8c22-fad6-4744-bb48-5e69b06c3ffd",
      "status": "CREATED"
    },
    {
      "accessPointId": """ + '"' + ap_id + '"' + """,
      "accessPointIndex": 2,
      "transmitPower": 0.0,
      "antennaTypeId": "7d534aad-6e83-4113-814a-a4dce1a07ee7",
      "antennaDirection": 0.0,
      "antennaTilt": 0.0,
      "antennaHeight": 2.4,
      "antennaMounting": "CEILING",
      "radioTechnology": "BLUETOOTH",
      "spatialStreamCount": 1,
      "shortGuardInterval": false,
      "defaultAntennas": [
        {
          "radioTechnology": "BLUETOOTH",
          "frequencyBand": "TWO",
          "antennaTypeId": "7d534aad-6e83-4113-814a-a4dce1a07ee7"
        }
      ],
      "enabled": true,
      "id": "e29849ed-c40a-44d7-97eb-ec31f77a3103",
      "status": "CREATED"
    },"""
    #Delete ',' in the end for the last entry
    RadioFile = RadioFile [:-1]
    #Write to file for every AP
    with open('simulatedRadios.json', 'a') as f:
        f.write(RadioFile)

    #End of file we need to create
    with open('simulatedRadios.json', 'a') as f:
        endofsimfile="""
    ]
}"""
        f.write(endofsimfile)
        f.close

    #Add created Files to the temporary directory (unzipped .esx File)
    shutil.copyfile('simulatedRadios.json','./' + myExtractfolder+'/simulatedRadios.json') 
    shutil.copyfile('antennaTypes.json','./' + myExtractfolder+'/antennaTypes.json') 

    #Delete created File
    os.remove('simulatedRadios.json')

    #Create .zip again ... because we have to replace some files
    shutil.make_archive(source, 'zip',  './' + myExtractfolder)
    #... and 'rename' it to .esx -> rename does not work because file with same name already exists
    shutil.copyfile(source +'.zip', myExtractfolder +'.esx') 
    #Delete .zip File after rename it as .esx
    os.remove(source +'.zip')

    #List needed Building/Floor - Structure for DNA-Center
    DNA_Structure_File.write('\nFile: ' + list_esx[x] + '\n')
    ###################################################################
    if not os.path.isfile(r"./" + myExtractfolder + '/buildings.json'):
        DNA_Structure_File.write("No Building defined in Ekahau!\n")
    else:
        with open('./' + myExtractfolder + '/buildings.json') as json_file:
            building_data = json.load(json_file)    
        #search for building
        for a in building_data['buildings']:
            building_name = a['name']
            DNA_Structure_File.write('\tBuilding: ' + building_name + "\n")
    
    with open('./' + myExtractfolder + '/floorPlans.json') as json_file:
        floor_data = json.load(json_file)    
    #search for Floors
    for a in floor_data['floorPlans']:
        floor_name = a['name']
        DNA_Structure_File.write('\t\tFloor: ' + floor_name + '\n')   
    DNA_Structure_File.write('\n=============================================\n')    
    DNA_Structure_File.close

    #Delete Folder
    shutil.rmtree('./' + myExtractfolder)
    print('Finished File: ' , list_esx[x])
    #Counter for next esx File in list
    x=x+1

MessageFinish="""Operation completed. 
Use the Files with '...Import_DNA.esx' for import in DNA-Center.
Also check the DNA-Structure.log in the directory for details about the Building/Floor Structure.

DO NOT USE THE CREATED ESX-FILES FOR DATA ANALYTICS IN EKAHAU! JUST FOR IMPORT!
"""
print(MessageFinish)   


