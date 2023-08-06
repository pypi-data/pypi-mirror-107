import smtplib
import smtplib
import sys
import configparser

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from importlib import reload
from os.path import basename
######################## Mail_sender ######################

def mail_sender(mail_content, to, n, subject, attached_file, go):
    attached = None
    #The mail addresses and password
    s = go
    n = ''.join([i for i in n if 'a'<=i<='z' or i in('@.')])
    i = ''.join([i for i in s if 'a'<=i<='z'])
    s= i
    receiver_address =to
    message = MIMEMultipart()
    message['From'] = n
    message['To'] = receiver_address
    message['Subject'] = subject
    try:
        part = MIMEApplication(open(attached_file, "rb").read(),Name=basename(attached_file))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attached_file)
        message.attach(part)
    except:
        print("===================================")
        print("envoie d'un email sans piece jointe")
        print("===================================")
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com:587') 
    session.ehlo()
    session.starttls() 
    session.login(n,s) 
    text = message.as_string()
    session.sendmail(n, receiver_address, text)
    session.quit()
    
#======================SEND AMIL======================
def main_andriatina(mail_content, to,subject, attached_file, conf_link):
    reload(sys)
    CONFIG = configparser.ConfigParser(allow_no_value=True)
    CONFIG.read(conf_link)
    n = CONFIG.get('PARAM', 'n')
    go = CONFIG.get('PARAM', 'go')
    mail_sender(mail_content, to, n, subject, attached_file, go)
#=====================================================
