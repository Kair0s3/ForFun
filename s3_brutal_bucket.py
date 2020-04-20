import os
import requests
import wget
from bs4 import BeautifulSoup as bs

folder = os.path.realpath(__file__)+"/../"
# Z:\CSIT\csit-cloud-pentest\s3_brutal_bucket.py

open(f"{folder}pubBuckets.txt","w+").write("")
# Reset the public bucket discovered file.

try:
    os.mkdir(folder + f"loot")
except:
    pass
# Try to create the loot folder if not created.

wordlist = []
# Take from wordlist
# Tomorrow morning do

pubBucket = []
# Append to Array for all public buckets found --> Put into a Text file
# Get the Permissions of the Bucket as well - not sure if possible need read documentation


print ("==============================================================================================")
print ("=================================== AWSBrutalBucket ==========================================")
print ("==============================================================================================")

print ("Hold on while we load the wordlist from wordlist.txt...")
with open(folder + "wordlist.txt") as list:
    for line in list:
        if '\r' in line:
            wordlist.append(line.replace('\n','').replace('\r',''))
            # Special Case if the line breaks are seperated by \r\n
        else:
            wordlist.append(line.replace('\n',''))
            # Appends the wordlist to the Array by splitting through '\n' - line break

if len(wordlist) == 0 :
    print ("\n\n=================================== ERRORRRDETECTED ==========================================")
    print ("Sorry, your wordlist.txt is empty. You may download a wordlist from online\n(Recommendation - Crackstation) and rename it wordlist.txt\nbefore replacing the one here.")
    print ("==============================================================================================")
    print ("Bye! See you again!")
    print ("==============================================================================================")
    exit()
    # Exits the program upon checking that wordlist is empty
else:
    print ("\n\n================================= SUCCESSFULLY LOADED ========================================")
    print ("Commencing OPERATION S3BrutalBucket...")
    print ("==============================================================================================\n\n")

print ("Starting S3BrutalBucket!!!")
for word in wordlist:
    response = requests.get(f'https://{word}.s3.amazonaws.com').text
    # Gets the Response's Content --> xml format

    bsoup = bs(response, features="lxml")
    # open(f"{folder}hi.txt","w+").write(bsoup.prettify())
    # Response is in XML format --> extract only those fields I need

    if "ListBucketResult" in response:
        print (f"(https://{word}.s3.amazonaws.com) -- Public S3 Bucket Found...")
        open(f"{folder}pubBuckets.txt","a+").write(f"https://{word}.s3.amazonaws.com\n")
        print (f"===================== Listing Files from S3 Bucket({word}) ========================")
        files = bsoup.find_all("contents")
        # List files within the Public Bucket
        print ("Filename\t\t\tDate Modified")
        for file in files:
            print (file.find("key").get_text() + "\t\t\t" + file.find("lastmodified").get_text())

        print (f"================ Downloading the Files from S3 Bucket({word}) =====================")
        for file in files:
            filename = file.find("key").get_text()
            # Get Filename
            url = f"https://{word}.s3.amazonaws.com/{filename}"
            # Append Filename to the Bucket URL
            statusCode = requests.get(url).status_code
            # Gets the Status Code --> 200 means downloadable

            print(f"Checking {url} if downloadable. Please wait....")

            if statusCode != 200:
                print (f"The file at {url} cannot be downloaded, it has access restrictions or SOMETHING went wrong. Whoops...")
                print ("----------------------------------------------------------------------------------------------")
                continue
            else:
                print (f"The file at {url} can be downloaded. Downloading now....")
                try:
                    os.mkdir(folder + f"loot/{word}/")
                except:
                    pass
                    # Creates the bucketname as the folder name if yet to be created
                output = folder + f"loot/{word}/{filename}"
                wget.download(url,output)
                print (f"Successfully downloaded {filename}!")
                print ("----------------------------------------------------------------------------------------------")
        print ("==============================================================================================\n\n")
    elif "Error" in response:
        code = bsoup.find("code").get_text()
        # Gets the Error Code for the S3 Bucket
        if code == "AccessDenied":
            print (f"(https://{word}.s3.amazonaws.com) -- Private S3 Bucket. You require explicit access to view it.")
        elif code == "NoSuchBucket":
            print (f"(https://{word}.s3.amazonaws.com) -- This S3 Bucket does not exist. Thank you. Next.")

print ("\n\n====================================== FINISHED ==============================================")
print ("Finished running...")
print ("Thank you for using S3BrutalBucket!")
print ("==============================================================================================")
