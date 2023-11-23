import socket
import Mail

defaultSubject = "Anh DuyTech"
defaultContent = "Anh DuyTech"

class Client_SMTP:
    def __init__(self, mailserver, port, username):
        self.mailserver = mailserver
        self.port = port
        self.username = username

        self.clientSocket: None
        
        self.endmsg = "\r\n.\r\n"

    def connectWithServer(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.mailserver, self.port))
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        self.__command_HELO()

    def sendEmail(self):
        mailTo = self.getMailTo()
        cc = self.getCC()
        bcc = self.getBCC()

        for recipient in mailTo + cc:
            self.sendOneMail(recipient, mailTo, cc, "", defaultSubject, defaultContent)

        for recipient in bcc:
            self.sendOneMail(recipient, mailTo, cc, recipient, defaultSubject, defaultContent)

    def sendOneMail(self, recipient: str, mailTo: list, cc: list, bcc: str, subject: str, content: str):        
        mail = Mail.Mail(
                sender= self.username,
                mailTo= mailTo,
                cc= cc,
                bcc= bcc,
                subject= subject,
                content = content
            )
        self.connectWithServer()
        self.__command_MAIL_FROM()
        self.__command_RCPT_TO(recipient)
        self.__command_DATA(mail.getMailContent())
        self.endSession()

    def getMailTo(self):
        mailTo = []
        while True:
            recipient = input("To (Press 0 to exit): ")
            if recipient == "0":
                break
            mailTo.append(recipient)
        return mailTo

    def getCC(self):
        cc = []
        while True:
            recipient = input("Add CC (Press 0 to exit): ")
            if recipient == "0":
                break
            cc.append(recipient)
        return cc

    def getBCC(self):
        bcc = []
        while True:
            recipient = input("Add BCC (Press 0 to exit): ")
            if recipient == "0":
                break
            bcc.append(recipient)
        return bcc

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
