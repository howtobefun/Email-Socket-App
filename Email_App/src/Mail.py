from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import mimetypes
import os

COMMASPACE = ", "
endmsg = "\r\n.\r\n"

class Mail:
    def __init__(self, sender: str, mailTo: list, cc: list, bcc: str, subject: str, content: str, filePath: str):
        self.message = MIMEMultipart()
        self.message["From"] = sender
        self.message["To"] = COMMASPACE.join(mailTo)
        self.message["Cc"] = COMMASPACE.join(cc)
        self.message["Bcc"] = bcc
        self.message["Subject"] = subject
        self.message.attach(MIMEText(content))  

        if (filePath != ""):
            attachment = self.getFileFromPath(path= filePath)
            if (attachment != None):
                self.message.attach(attachment)

    def getFileFromPath(self, path: str):
        with open(path, "rb") as file:
            basename = os.path.basename(path)
            attachment = MIMEApplication(file.read(), Name= basename)
            attachment['Content-Disposition'] = f'attachment; filename= "{basename}"'
            return attachment

    def getMailContent(self):
        return self.message.as_string()
    