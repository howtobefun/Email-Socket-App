from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os

COMMASPACE = ", "
END_MSG = "\r\n.\r\n"

class Mail:
    def __init__(self, sender: str, mail_to: list, cc: list, bcc: str, subject: str, content: str, file_paths: str):
        self.message = MIMEMultipart()
        self.message["From"] = sender
        self.message["To"] = COMMASPACE.join(mail_to)
        self.message["Cc"] = COMMASPACE.join(cc)
        self.message["Bcc"] = bcc
        self.message["Subject"] = subject
        self.message.attach(MIMEText(content))  

        if file_paths != "":
            attachments = self.get_files_from_path(paths=file_paths)
            if attachments:
                for attachment in attachments:
                    self.message.attach(attachment)

    def get_files_from_path(self, paths: str):
        file_list = paths.split(COMMASPACE)
        attachments = []
        for path in file_list: 
            if not path:
                continue
            with open(path, "rb") as file:
                basename = os.path.basename(path)
                attachment = MIMEApplication(file.read(), Name=basename)
                attachment['Content-Disposition'] = f'attachment; filename= "{basename}"'
                attachments.append(attachment)
        
        return attachments

    def get_mail_content(self):
        return self.message.as_string()
