from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import argparse


# Parse the passed arguments
parser = argparse.ArgumentParser()
parser.add_argument("files", help="List files to be uploaded.", nargs="+")

# Define the credentials folder
home_dir = os.path.expanduser("~")
credential_dir = os.path.join(home_dir, ".credentials")
if not os.path.exists(credential_dir):
    os.makedirs(credential_dir)
credential_path = os.path.join(credential_dir, "pydrive-credentials.json")

# Start authentication
gauth = GoogleAuth()
gauth.CommandLineAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile(credential_path)
gauth.CommandLineAuth() 
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.CommandLineAuth() 
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile(credential_path)