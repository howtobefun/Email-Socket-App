endmsg = "\r\n.\r\n"

class Mail:
    def __init__(self, sender: str, mailTo: list, cc: list, bcc: list, title: str, content: str):
        self.mailFrom = sender
        self.mailTo = mailTo
        self.cc = cc
        self.bcc = bcc
        self.title = title
        self.content = content

    def getMailTo(self):
        return self.mailTo
    def getCC(self):
        return self.cc
    def getBCC(self):
        return self.bcc
    def getTitle(self):
        return self.title
    def getContent(self):
        return self.content

    def getMailContent(self, bcc: str):
        content = ""
        content += f"From: {self.mailFrom}\r\n"
        
        content += "To:"
        for recipient in self.mailTo:
            content += f" {recipient}"
        content += "\r\n"

        content += "CC:"
        for recipient in self.cc:
            content += f" {recipient}"
        content += "\r\n"

        content += f"BCC: {bcc}\r\n"

        content += f"Title: {self.title}\r\n"

        content += f"Content: {self.content}"

        return content