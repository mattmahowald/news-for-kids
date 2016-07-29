#!/home/ec2-user/.virtualenvs/news-4-kids/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
from datetime import datetime
import os
import shutil
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import argparse


URL = 'http://cache.newsomatic.net/dynamicv2/content/files/feed.php?format=json&token=FreJPn2ZcFXS3NVu' 

HEADERS = ["Headline",
    "Subheadline",
    "MainArticle",
    "MainArticle1-2",
    "MainArticle5-6",
    "MainArticleSpanish"]

class Article:

    def __init__(self, json_content):
        self.headline = json_content["Headline"]
        self.subhead = json_content["Subheadline"]
        self.main = json_content["MainArticle"]
        self.main_low = json_content["MainArticle1-2"]
        self.main_mid = json_content["MainArticle5-6"]
        self.main_span = json_content["MainArticleSpanish"]
        
    def get_all(self):
        return [self.headline, self.subhead, self.main, 
                    self.main_low, self.main_mid, self.main_span]

def get_json_data(URL):
    r = requests.get(URL)
    return r.json()
    
def format_spanish(spanish_html):
    spanish_html = spanish_html.replace('<b>', '<h1 id=\"mainhead\">', 1)
    spanish_html = spanish_html.replace('\n<i>', '</h1>\n\n<h2 id=\"deckhead\">', 1)
    spanish_html = spanish_html.replace('</i></b>', '</h2>\n\n<p>', 1)
    return spanish_html


files = []
def write_to_html(date, articles):
    for a, n in zip(articles, range(1,len(articles) + 1)):
        data = a.get_all()
        h = data[0]
        h2 = data[1]
        types = ['c_advanced', 'b_intermediate', 'a_starter', 'd_spanish']
        for i, t in zip(range(2,1+len(types)), types):
            name = '{}_{}{}.html'.format(date, n, t)
            with open(name, 'w') as htmlfile:
                htmlfile.write("<h1 id=\"mainhead\">{}</h1>\n\n".format(h))
                htmlfile.write("<h2 id=\"deckhead\">{}</h2>\n\n".format(h2))
                htmlfile.write("<p>{}</p>".format(data[i]))
            files.append(name)
        name = '{}_{}d_spanish.html'.format(date, n)
        with open(name, 'w') as htmlfile:
                htmlfile.write("{}</p>".format(format_spanish(data[5])))
        files.append(name)
            
def upload_to_gdrive(folder_name):
    PARENT_ID = "0B9AS7owE5ZT9NWNfVk9FRkFCNzA"
    
    # Define the credentials folder
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "pydrive-credentials.json")

    # Start authentication
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile(credential_path)
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

    drive = GoogleDrive(gauth)


    file_metadata = {
      "parents": [{"id": PARENT_ID}],
      'title' : folder_name,
      'mimeType' : 'application/vnd.google-apps.folder'
    }

    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    folder_id = folder.get('id')
    print(folder)

    # Upload the files
    for f in files:
        new_file = drive.CreateFile({"parents": [{"id": folder_id}], 
                                                  "mimeType":"text/plain"})
        new_file.SetContentFile(f)
        new_file.Upload()


def main():
    date = "{:%Y%m%d}".format(datetime.now())
    folder = "/home/ec2-user/code/news-4/{}".format(os.getcwd(), date)
    if(os.path.exists(folder)):
        shutil.rmtree(folder)
    os.mkdir(folder)
    os.chdir(folder)
    data = get_json_data(URL)
    articles = [Article(content) for content in data]
    write_to_html(date, articles)
    upload_to_gdrive(date)

if __name__ == '__main__':
    main()
