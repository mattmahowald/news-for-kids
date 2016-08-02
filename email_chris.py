import smtplib
from datetime import date

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import random

# AWS Config
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_HOST_USER = 'AKIAIY3ZMG72GQS35G6A'
EMAIL_HOST_PASSWORD = 'AperlrZzeFcE5Exbl94/bYTNQjhU4illDByhWvlsqkir' 
EMAIL_PORT = 587

d = date.today()

msg = MIMEMultipart('alternative')
msg['Subject'] = "{}".format(random.random()) 
msg['From'] = "mcm2018@stanford.edu"
msg['To'] = "chris@lightsailed.com"


filep = '/home/ec2-user/code/news-4-kids.png' 
fp = open(filep, 'rb')
img = MIMEImage(fp.read())
fp.close()
msg.attach(img)

s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
s.starttls()
s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
