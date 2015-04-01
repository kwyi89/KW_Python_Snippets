
# coding: utf-8

# In[2]:

# account setup
username = '***';
password = '***';
server = 'smtp.gmail.com:587';

# imports
from time import sleep
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# create msg - MIME* object
# takes addresses to, from cc and a subject
# returns the MIME* ojbect
def create_msg(to_address,
               from_address='',
               cc_address='',
               bcc_address='',
               subject=''):
    msg = MIMEmultipart()
    msg['Subject'] = subject
    msg['To'] = to_address
    msg['From'] = from_address
    msg['Cc'] = cc_address
    return msg

# send an email
# takes an smtp address, username, password and MIME* object
# if mode = 0 sends to and cc
# if mode = 1 sends to bcc
def send_email(smtp_address, usr, password, msg, mode):
    server = smtplib.SMTP(smtp_address)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    if (mode == 0 and msg['To'] != ''):
        server.sendmail(msg['From'],(msg['To']+msg['Cc']).split(","), msg.as_string())
    elif (mode == 1 and msg['Bcc'] != ''):
        server.sendmail(msg['From'],msg['Bcc'].split(","),msg.as_string())
    elif (mode != 0 and mode != 1):
        print 'error in send mail bcc'
        print 'email cancelled'
        exit()
    server.quit()
    
### compose email    

