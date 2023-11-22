from client_POP3 import *
from client_SMTP import *

mailserver = "127.0.0.1"
SMTPport = 2225
POP3port = 3335
sender = "AnhDuyTech@DuyTech.DuyTech"
recipient = "Duy@Duy.Duy"

if __name__ == "__main__":
    username = sender
    password = "password"

    SMTPclient = Client_SMTP(mailserver, SMTPport, username)
    SMTPclient.sendEmail()

    # POP3client = Client_POP3(mailserver, POP3port, recipient, password)
    # POP3client.showNumberOfMails()
