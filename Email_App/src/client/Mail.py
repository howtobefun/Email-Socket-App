from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os

COMMASPACE = ", "
endmsg = "\r\n.\r\n"

class Mail:
    def __init__(self, sender: str, mailTo: list, cc: list, bcc: str, subject: str, content: str, filePaths: str):
        self.message = MIMEMultipart()
        self.message["From"] = sender
        self.message["To"] = COMMASPACE.join(mailTo)
        self.message["Cc"] = COMMASPACE.join(cc)
        self.message["Bcc"] = bcc
        self.message["Subject"] = subject
        self.message.attach(MIMEText(content))  

        if (filePaths != ""):
            attachments = self.getFileFromPath(paths= filePaths)
            if (attachments != []):
                for attachment in attachments:
                    self.message.attach(attachment)

    def getFileFromPath(self, paths: str):
        fileList = paths.split(COMMASPACE)
        attachments = []
        for path in fileList: 
            if (path == ""):
                continue
            with open(path, "rb") as file:
                basename = os.path.basename(path)
                attachment = MIMEApplication(file.read(), Name= basename)
                attachment['Content-Disposition'] = f'attachment; filename= "{basename}"'
                attachments.append(attachment)
        
        return attachments

    def getMailContent(self):
        return self.message.as_string()