from client_POP3 import *
from client_SMTP import *
import json
import os
from types import SimpleNamespace

def init_config_data():
    config_file_path = 'src/config/config.json'
    with open(config_file_path) as fp:
        config_data_object = json.load(fp, object_hook=lambda d: SimpleNamespace(**d))

    return config_data_object

if __name__ == "__main__":
    UI_PATH = os.path.dirname(__file__)
    os.chdir(UI_PATH + '/../../')
    
    config_data_object = init_config_data()

    username = config_data_object.General.username
    password = config_data_object.General.password
    mailserver = config_data_object.Mailserver.ServerIP
    SMTPport = config_data_object.Mailserver.SMTPport
    POP3port = config_data_object.Mailserver.POP3port

    # SMTPclient = Client_SMTP(mailserver, SMTPport, username)
    # SMTPclient.sendEmail("duy", "", "", "duytech", "")

    username = "123"
    pop3_client = Client_POP3(mailserver, POP3port, username, password)
    pop3_client.show_number_of_mails()
    pop3_client.show_list_mails()
    pop3_client.retrieve_all_mails()
    print(pop3_client.get_all_mail_header())
