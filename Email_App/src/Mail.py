from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ", "
endmsg = "\r\n.\r\n"

class Mail:
    def __init__(self, sender: str, mailTo: list, cc: list, bcc: str, subject: str, content: str):
        self.message = MIMEMultipart()
        self.message["From"] = sender
        self.message["To"] = COMMASPACE.join(mailTo)
        self.message["Cc"] = COMMASPACE.join(cc)
        self.message["Bcc"] = bcc
        self.message["Subject"] = subject
        self.message.attach(MIMEText(content))

    def getMailContent(self):
        return self.message.as_string()
    