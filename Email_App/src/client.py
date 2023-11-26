from client_POP3 import *
from client_SMTP import *
import json
from types import SimpleNamespace

def initUser():
    configDataObject = initConfigData()
    username = configDataObject.General.username
    password = configDataObject.General.password
    mailserver = configDataObject.Mailserver.ServerIP
    SMTPport = configDataObject.Mailserver.SMTPport
    POP3port = configDataObject.Mailserver.POP3port

    SMTPclient = Client_SMTP(mailserver, SMTPport, username)
    return SMTPclient

def initConfigData():
    configFilePath = 'config/config.json'
    with open(configFilePath) as fp:
        configDataObject = json.load(fp, object_hook=lambda d: SimpleNamespace(**d))

    return configDataObject

if __name__ == "__main__":
    configDataObject = initConfigData()
    
    username = configDataObject.General.username
    password = configDataObject.General.password
    mailserver = configDataObject.Mailserver.ServerIP
    SMTPport = configDataObject.Mailserver.SMTPport
    POP3port = configDataObject.Mailserver.POP3port

    # SMTPclient = Client_SMTP(mailserver, SMTPport, username)
    # SMTPclient.sendEmail("duy","","","duytech","")

    POP3client = Client_POP3(mailserver, POP3port, username, password)
    POP3client.retrieveFirstMail()
    POP3client.retrieveAttachments()
