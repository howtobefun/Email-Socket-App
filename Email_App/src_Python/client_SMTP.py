import socket

class Client_SMTP:
    def __init__(self, mailserver, port, username):
        self.mailserver = mailserver
        self.port = port
        self.username = username

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((mailserver, port))
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

        self.endmsg = "\r\n.\r\n"

        self.__command_HELO()

    def sendEmail(self, recipient):
        self.__command_MAIL_FROM()
        self.__command_RCPT_TO(recipient)
        self.__command_DATA("Anh DuyTech")

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