import socket

class Client_POP3:
    def __init__(self, mailserver, port):
        self.mailserver = mailserver
        self.port = port

        self.clientSocket = socket.socket()
        self.clientSocket.connect((mailserver, port))
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

        username = input("Username: ")
        password = input("Password: ")

        self.username = username
        self.password = password

    def command_USER(self):
        userCommand = f"USER {self.username}\r\n"
        self.clientSocket.send(userCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def command_PASS(self):
        passCommand = f"PASS {self.password}\r\n"
        self.clientSocket.send(passCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def command_STAT(self):
        statCommand = "STAT\r\n"
        self.clientSocket.send(statCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)

    def command_RETR(self):
        retrCommand = "RETR 1\r\n"
        self.clientSocket.send(retrCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        print(recv)
