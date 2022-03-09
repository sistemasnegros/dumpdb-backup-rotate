# -*- coding: utf-8 -*-
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

import smtplib


class Mail(object):

    def __init__(self, **kwargs):
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.server = kwargs["server"] + ":" + kwargs["port"]
        self.tls = kwargs["tls"]

    def send(self, **kwargs):
        listTo = kwargs["to"].split(",")
        msg = MIMEMultipart()
        msg['From'] = self.username
        
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = kwargs["subject"]

        msg.attach(MIMEText(kwargs["body"], 'plain', 'utf-8'))
        smtp = smtplib.SMTP(self.server)

        if self.tls:
            smtp.starttls()

        smtp.login(self.username, self.password)

        for to in listTo:
            msg['To'] = to 
            smtp.sendmail(kwargs["username"], to, msg.as_string())
        smtp.close()
