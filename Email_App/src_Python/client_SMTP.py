import socket

class Client_SMTP:
    def __init__(self, mailserver, port):
        user = input("Input sender: ")

        self.mailserver = mailserver
        self.port = port
        self.user = user

        self.clientSocket = socket.socket()
        self.clientSocket.connect((mailserver, port))
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

        self.endmsg = "\r\n.\r\n"

    def sendEmail(self, recipient):
        self.command_HELO()
        self.command_MAIL_FROM()
        self.command_RCPT_TO(recipient)
        self.command_DATA("Anh DuyTech")
        self.command_QUIT()


    def command_HELO(self):
        heloCommand = f'EHLO [{self.mailserver}]\r\n'
        self.clientSocket.send(heloCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def command_MAIL_FROM(self):
        mailFromCommand = f"MAIL FROM: {self.user}\r\n"
        self.clientSocket.send(mailFromCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
	
    def command_RCPT_TO(self, recipient):
        rcptToCommand = f"RCPT TO: {recipient}\r\n"
        self.clientSocket.send(rcptToCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
	
    def command_DATA(self, msg):
        dataCommand = "DATA\r\n"
        self.clientSocket.send(dataCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
        if (recv[:3] == '354'):
            sendmsg = msg + self.endmsg
            self.clientSocket.send((sendmsg).encode())
            self.clientSocket.recv(1024)

    def command_QUIT(self):
        quit_command = "QUIT\r\n"
        self.clientSocket.send(quit_command.encode())
        self.clientSocket.recv(1024)
        self.clientSocket.close()