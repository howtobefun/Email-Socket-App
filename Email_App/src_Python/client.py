from client_POP3 import *
from client_SMTP import *

mailserver = "127.0.0.1"
SMTPport = 2225
POP3port = 3335
sender = "Anh DuyTech"
recipient = "Duy"

if __name__ == "__main__":
    SMTPclient = Client_SMTP(mailserver, SMTPport)
    SMTPclient.sendEmail(recipient)
