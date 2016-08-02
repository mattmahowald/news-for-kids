#!/home/ec2-user/.virtualenvs/news-4-kids/bin/python3
# -*- coding: utf-8 -*-

'''File: news-4-kids.py
Accesses the news-o-matic API to parse relevant files and upload to GDrive.
'''

from __future__ import print_function

__author__ = "Matt Mahowald"
__email__  = "mcm2018@stanford.edu"

from datetime import datetime
import argparse
import os
import sys
import shutil
import requests
import re
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# URL for the newsomatic feed
URL = 'http://cache.newsomatic.net/dynamicv2/content/files/feed.php?format=json&token=FreJPn2ZcFXS3NVu' 

# Arbitrary headline ID for the header dictionary
HEADLINE_ID = 'h1'
SUBHEAD_ID = 'h2'

# The names and IDs for the four separate types of article
STARTER = "starter"
INTERMEDIATE = "intermediate"
ADVANCED = "advanced"
SPANISH = "spanish"

# A list of the article IDs for iteration
TYPES = [STARTER, INTERMEDIATE, ADVANCED, SPANISH]

# A dictionary for easy and clear index into the json dictionary
# These get updated by newsomatic unfortunately. If they are updated
# a corresponding error message will print to the log.
HEADERS = {HEADLINE_ID : "Headline",
    SUBHEAD_ID : "Subheadline",
    STARTER : "MainArticle1-2",
    INTERMEDIATE : "MainArticle3-4",
    ADVANCED : "MainArticle5-6",
    SPANISH : "MainArticleSpanish"}

TEST = True

# The parent folder id for the google drive. To replace this,
# go to the google drive belonging to the newsforkids user
#     username: newsforkids
#     password: literacy
# and navigate to the daily emails folder (or the folder that
# you want the emails to be placed under) and copy and past
# the folder ID from the link, which is identifiable as the
# last portion of the link.
#     e.g. https://drive.google.com/drive/u/2/folders/<ID here>
PARENT_ID = "0B9AS7owE5ZT9NWNfVk9FRkFCNzA"

def strip_html(data):
    '''Useful function to strip html tags from a string'''

    p = re.compile(r'<.*?>')
    return p.sub('', data)

class Article:
    '''Article object holds a single article's contents'''

    def _format_spanish(self, content):
        '''Internal method used to parse a Spanish article's json'''

        self.headline = strip_html(content.pop(0))
        self.subhead = strip_html(content.pop(0))
        self._format(content)

    def _format(self, content):
        '''Internal method used to parse a general article's json'''

        self.byline = strip_html(content.pop())
        self.date = strip_html(content.pop())
        self.body = content

    def __init__(self, article_content, headline, subhead, is_spanish=False):
        '''Creates an article object from json content'''

        content = list(filter(None, article_content.splitlines()))
        if is_spanish:
            self._format_spanish(content)
        else:
            self.headline = headline
            self.subhead = subhead
            self._format(content)

    def get_html(self):
        '''Returns the string for a single Article's HTML'''

        html = []
        html.append("<h1 id=\"mainhead\">{}</h1>".format(self.headline))
        html.append("<h2 id=\"deckhead\">{}</h2>".format(self.subhead))
        html += ["<p>{}</p>".format(p) for p in self.body]
        html.append(str("<p><small>{}\n<br/>\n"
                    "<i>{}</i></p></small>".format(self.date, self.byline)))
        html.append("".format(self.byline))
        return '\n\n'.join(html)

class Feed:

    def __init__(self, json_content):
        '''Creates a feed object for newsomatic articles'''

        headline = json_content[HEADERS[HEADLINE_ID]]
        subhead = json_content[HEADERS[SUBHEAD_ID]]

        try:
            self.articles = [Article(json_content[HEADERS[t]],
                    headline,
                    subhead,
                    is_spanish = t == SPANISH     
                ) for t in TYPES
            ]
        except KeyError as e:
            error_msg = str('\nThis error most likely occured because of\n'
                            'an issue with the headers in the json.\n'
                            'RECEIVED\tEXPECTED\n'
                            )
            for h1,h2 in zip(sorted(json_content), sorted(HEADERS.values())):
                error_msg += "{}\t{}\n".format(h1, h2)
            print(error_msg)
            email_warning(error_msg) 
            sys.exit(0)

    def get_all(self):
        '''Returns a list of the html for every article in a feed'''

        return [a.get_html() for a in self.articles]


def get_json_data(URL):
    '''Returns the json data for the passed in url'''

    r = requests.get(URL)
    return r.json()

def write_to_html(date, feeds):
    '''Writes content to a temporary folder in the current directory'''

    for f, feed_num in zip(feeds, range(len(feeds))):
        for html, article_num in zip(f.get_all(), 
                                     range(len(f.articles))):
            ch = chr(ord('a') + article_num)
            name = '{}_{}{}_{}.html'.format(date,
                                                feed_num + 1, 
                                                ch, 
                                                TYPES[article_num]
                                            )
            with open("{}/{}".format(date, name), 'w') as htmlfile:
                htmlfile.write(html)

def email_warning(error_msg=""):
    '''Sends an email to Chris if program goes down'''
    if not cron_flag:
        return
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # AWS Config
    EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
    EMAIL_HOST_USER = 'AKIAIY3ZMG72GQS35G6A'
    EMAIL_HOST_PASSWORD = 'AperlrZzeFcE5Exbl94/bYTNQjhU4illDByhWvlsqkir' 
    EMAIL_PORT = 587

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'News for Kids is Down' 
    msg['From'] = "mmahowald@lightsailed.com"
    msg['To'] = "mmahowald@lightsailed.com"

    content = MIMEText(error_msg, 'plain')
    msg.attach(content)

    s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

def upload_to_gdrive(folder_name, folder_path, drive, cron=False):
    '''Exports files to Google Drive'''

    file_metadata = {
      "parents": [{"id": PARENT_ID}],
      'title' : folder_name,
      'mimeType' : 'application/vnd.google-apps.folder'
    }

    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    folder_id = folder.get('id')

    # Upload the files
    files = os.listdir(folder_path)
    for f in files:
        print("uploading file {}".format(f))
        new_file = drive.CreateFile({"parents" : [{"id": folder_id}], 
                                     "mimeType" : "text/plain",
                                     "title" : f})
        new_file.SetContentFile(os.path.join(folder_path, f))
        new_file.Upload()
    if cron:
        print('Successfully parsed articles for {}'.format(folder_name))
        error_log = drive.CreateFile({"parents" : [{"id": folder_id}], 
                                         "mimeType" : "text/plain"})
        error_log.SetContentFile('.newsforkids_errorlog.txt')
        error_log.Upload()

def authenticate_gdrive():
    '''Authenticates machine for Google Drive use'''

    # Define the credentials folder
    credential_dir = os.path.join(os.getcwd(), ".credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "pydrive-credentials.json")

    # Start authentication
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile(credential_path)
    if gauth.credentials is None:
        if cron:
            error_msg = "This machine is not authenticated."
            email_warning(error_msg)
            sys.exit(0)

        print(str("You are not authenticated to write to GDrive.\n"
            "In order to authenticate, follow the below instructions.\n"
            "Once completed, you should be authenticated to write to GDrive\n"))
        gauth.CommandLineAuth() 
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile(credential_path)

    return GoogleDrive(gauth)

def create_folder():
    '''Creates a temporary folder for the current day's articles'''

    date = "{:%Y%m%d}".format(datetime.now())
    folder_path = os.path.join(os.getcwd(), date)
    if(os.path.exists(folder_path)):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)
    return date, folder_path

cron_flag = False

def main():
    if TEST:
        PARENT_ID = "0B4sUJlbVBodvemNHcFRwMlAtUTg" 
    # the cron_flag is a hack and should probably be cleaned up
    cron_flag = sys.argv[-1] == '-c'
    if cron_flag:
        sys.stdout = open('.newsforkids_errorlog.txt', 'w')
    drive = authenticate_gdrive()
    date, folder_path = create_folder()
    data = get_json_data(URL)
    feeds = [Feed(content) for content in data]
    print(feeds)
    write_to_html(date, feeds)
    upload_to_gdrive(date, folder_path, drive, cron=cron_flag)
    shutil.rmtree(folder_path)

if __name__ == '__main__':
    main()