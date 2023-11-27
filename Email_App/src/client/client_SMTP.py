import socket
import Mail

defaultSubject = "Anh DuyTech"
defaultContent = "Anh DuyTech"
defaultFilePath = ""

class Client_SMTP():
    def __init__(self, mailserver, port, username, password, email):
        self.mailserver = mailserver
        self.port = port
        self.username = username
        self.email = email

        self.clientSocket: None
        
        self.endmsg = "\r\n.\r\n"

    def connectWithServer(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.mailserver, self.port))
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        self.__command_HELO()

    def sendEmail(self, mailTo_str: str, cc_str: str, bcc_str: str, subject: str, content: str):
        mailTo = self.getMailTo(mailTo_str)
        cc = self.getCC(cc_str)
        bcc = self.getBCC(bcc_str)

        for recipient in mailTo + cc:
            self.sendOneMail(recipient, mailTo, cc, "", subject, content, defaultFilePath)

        for recipient in bcc:
            self.sendOneMail(recipient, mailTo, cc, recipient, subject, content, defaultFilePath)

    def sendOneMail(self, recipient: str, mailTo: list, cc: list, bcc: str, subject: str, content: str, filePath: str):        
        mail = Mail.Mail(
                sender= self.email,
                mailTo= mailTo,
                cc= cc,
                bcc= bcc,
                subject= subject,
                content = content,
                filePath= filePath
            )
        self.connectWithServer()
        self.__command_MAIL_FROM()
        self.__command_RCPT_TO(recipient)
        self.__command_DATA(mail.getMailContent())
        self.endSession()

    def getMailTo(self, mailTo_str: str):
        if mailTo_str != "":
            mailTo = mailTo_str.split(Mail.COMMASPACE)
            return mailTo
        return []
    
    def getCC(self, cc_str: str):
        if cc_str != "":
            cc = cc_str.split(Mail.COMMASPACE)
            return cc
        return []

    def getBCC(self, bcc_str: str):
        if bcc_str != "":
            bcc = bcc_str.split(Mail.COMMASPACE)
            return bcc
        return []

    def endSession(self):
        self.__command_QUIT()
        self.clientSocket.close()

    def __command_HELO(self):
        command = f'EHLO [{self.mailserver}]\r\n'
        self.clientSocket.send(command.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def __command_MAIL_FROM(self):
        command = f"MAIL FROM: <{self.username}>\r\n"
        self.clientSocket.send(command.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
	
    def __command_RCPT_TO(self, recipient):
        command = f"RCPT TO: <{recipient}>\r\n"
        self.clientSocket.send(command.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
	
    def __command_DATA(self, msg):
        command = "DATA\r\n"
        self.clientSocket.send(command.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if (recv[:3] == '354'):
            sendmsg = msg + self.endmsg
            self.clientSocket.send((sendmsg).encode())
            self.clientSocket.recv(1024)

    def __command_QUIT(self):
        command = "QUIT\r\n"
        self.clientSocket.send(command.encode())
        self.clientSocket.recv(1024)

if __name__ == "__main__":
    pass