from client_POP3 import *
from client_SMTP import *
import json
import os
from types import SimpleNamespace

def initSMTPClient():
    configDataObject = initConfigData()
    username = configDataObject.General.username
    password = configDataObject.General.password
    mailserver = configDataObject.Mailserver.ServerIP
    SMTPport = configDataObject.Mailserver.SMTPport
    POP3port = configDataObject.Mailserver.POP3port

    SMTPclient = Client_SMTP(mailserver, SMTPport, username, password, username)
    return SMTPclient

def initConfigData():
    configFilePath = 'src/config/config.json'
    with open(configFilePath) as fp:
        configDataObject = json.load(fp, object_hook=lambda d: SimpleNamespace(**d))

    return configDataObject

if __name__ == "__main__":
    UI_PATH = os.path.dirname(__file__)
    os.chdir(UI_PATH + '/../../')
    
    configDataObject = initConfigData()

    username = configDataObject.General.username
    password = configDataObject.General.password
    mailserver = configDataObject.Mailserver.ServerIP
    SMTPport = configDataObject.Mailserver.SMTPport
    POP3port = configDataObject.Mailserver.POP3port

    # SMTPclient = Client_SMTP(mailserver, SMTPport, username)
    # SMTPclient.sendEmail("duy","","","duytech","")

    username = "123"
    POP3client = Client_POP3(mailserver, POP3port, username, password)
    POP3client.showNumberOfMails()
    POP3client.showListMails()
    POP3client.retrieveAllMails()
