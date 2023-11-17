import socket

class Client_SMTP:
    def __init__(self, mailserver, port, username):
        self.mailserver = mailserver
        self.port = port
        self.username = "<" + username + ">"

        self.clientSocket = socket.socket()
        self.clientSocket.connect((mailserver, port))
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

        self.endmsg = "\r\n.\r\n"

        self.__command_HELO()

    def sendEmail(self, recipient):
        self.__command_MAIL_FROM()
        self.__command_RCPT_TO("<" + recipient + ">")
        self.__command_DATA("Anh DuyTech")
    
    def endSession(self):
        self.__command_QUIT()
        self.clientSocket.close()

    def __command_HELO(self):
        heloCommand = f'EHLO [{self.mailserver}]\r\n'
        self.clientSocket.send(heloCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def __command_MAIL_FROM(self):
        mailFromCommand = f"MAIL FROM: {self.username}\r\n"
        self.clientSocket.send(mailFromCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
	
    def __command_RCPT_TO(self, recipient):
        rcptToCommand = f"RCPT TO: {recipient}\r\n"
        self.clientSocket.send(rcptToCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
	
    def __command_DATA(self, msg):
        dataCommand = "DATA\r\n"
        self.clientSocket.send(dataCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if (recv[:3] == '354'):
            sendmsg = msg + self.endmsg
            self.clientSocket.send((sendmsg).encode())
            self.clientSocket.recv(1024)

    def __command_QUIT(self):
        quit_command = "QUIT\r\n"
        self.clientSocket.send(quit_command.encode())
        self.clientSocket.recv(1024)