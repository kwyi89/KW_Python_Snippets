
# coding: utf-8

# In[7]:

# Date and Time Script
# Use this to parse date and time

from datetime import datetime

now = datetime.now()
mm=str(now.month)
dd=str(now.day)
yyyy=str(now.year)
hour=str(now.hour)
mi=str(now.minute)
ss=str(now.second)

print mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss


# In[8]:

# Sending out email with Python
# smtplib module defines an SMTP client session object that can be used to send email.
# SMTP stand for Simple Mail Transfer Protocol

import smtplib
server=smtplib.SMTP('smtp.gmail.com',587)

server.login("youremailaccount","password")

msg = "\nHello!"
serversendmail("you@gmail.com","target@example.com",msg)


# In[9]:

# Since smtplib is too simple, we will use email module
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

fromaddr = "you@gmail.com"
toaddr = "target@example.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Python email"

body = "Python test mail body"
msg.attach(MIMEText(body, 'plain'))

import smtplib
server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("youremailusername","password")
text = msg.as_string()
server.sendmail(fromaddr,toaddr,text)


# In[11]:

# Example sending emails using Gmail
import smtplib

def sendemail(from_addr,to_addr_list,cc_addr_list,
    subject, message,
    login, password,
    smtpserver = 'smtp.gmail.com:587'):
    header = 'From: %s\n'%from_addr
    header+= 'To: %s\n'%join(to_addr_list)
    header+= 'Cc: %s\n'%join(cc_addr_list)
    header+='Subject: %s\n\n' % subject
    message = header + message
    
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    sever.login(login,password)
    problems = server.sendmail(from_addr,to_addr_list,message)
    server.quit()


# In[ ]:



