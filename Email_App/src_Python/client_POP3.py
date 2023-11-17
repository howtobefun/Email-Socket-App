import socket

class Client_POP3:
    def __init__(self, mailserver, port, username, password):
        self.mailserver = mailserver
        self.port = port

        self.clientSocket = socket.socket()
        self.clientSocket.connect((mailserver, port))
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

        self.username = username
        self.password = password

        self.__command_USER()
        self.__command_PASS()

    def showNumberOfMails(self):
        self.__command_STAT()
    
    def endSession(self):
        self.__command_QUIT()
        self.clientSocket.close()
        
    def __command_USER(self):
        userCommand = f"USER {self.username}\r\n"
        self.clientSocket.send(userCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def __command_PASS(self):
        passCommand = f"PASS {self.password}\r\n"
        self.clientSocket.send(passCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def __command_STAT(self):
        statCommand = "STAT\r\n"
        self.clientSocket.send(statCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def __command_RETR(self):
        retrCommand = "RETR 1\r\n"
        self.clientSocket.send(retrCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def __command_QUIT(self):
        QUITcommand = "QUIT \r\n"
        self.clientSocket.send(QUITcommand.encode())
        self.clientSocket.recv(1024)
