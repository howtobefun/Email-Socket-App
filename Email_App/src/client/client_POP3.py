import socket
import os
from email import message_from_bytes
import time

savePath = "attachments/"
MAILBOX_PATH = "User_Mailbox/"
SERVER_MAILBOX_PATH = "../Test_Server/"

def remove_extension(file_path):
        root, extension = os.path.splitext(file_path)
        return root

class Client_POP3:
    def __init__(self, mailserver, port, username, password):
        self.mailserver = mailserver
        self.port = port
        self.clientSocket = None

        self.username = username
        self.password = password

        self.numberOfMails = None

        self.recvData = None
        self.email_message = None
        self.msgID = None

        dir_path = os.path.join(SERVER_MAILBOX_PATH, username)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        self.serverMails = os.listdir(dir_path)

        self.USER_MAILBOX = MAILBOX_PATH + self.username + "/"

    def showNumberOfMails(self):
        self.__connectWithServer()
        self.__command_STAT()
        self.endSession()

    def showListMails(self):
        self.__connectWithServer()
        self.__command_LIST()
        self.endSession()

    def retrieveAllMails(self):
        if (self.numberOfMails == None):
            return
        for i in range(1, int(self.numberOfMails) + 1):
            self.__connectWithServer()
            self.retrieveMail(mailNumber=i)
            self.endSession()
    
    def retrieveMail(self, mailNumber=1):
        self.__retrieveMailMessage(mailNumber)
        self.__retrieveAttachments()

    def __connectWithServer(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.mailserver, self.port))
        self.clientSocket.settimeout(5)
        recv = self.clientSocket.recv(1024).decode()
        self.__command_USER()
        self.__command_PASS()

    def __retrieveMailMessage(self, mailNumber=1):
        self.recvData = self.__command_RETR(mailNumber=mailNumber)
        recv_message = self.recvData[(self.recvData.find("\r\n".encode()) + 2):]
        self.email_message = message_from_bytes(recv_message)
        self.__transferMailMessageToMailBox()

    def __transferMailMessageToMailBox(self):
        if not os.path.exists(self.USER_MAILBOX):
            os.mkdir(self.USER_MAILBOX)

        with open(self.USER_MAILBOX + f"/{self.msgID}.txt", "w") as fp:
            for part in self.email_message.walk():
                if part.get_content_type() == 'text/plain':
                    fp.write(part.get_payload(decode=True).decode())

    
    def __retrieveAttachments(self):
        if self.email_message.is_multipart():
            for part in self.email_message.walk():
                if part.get_content_type() == 'text/plain':
                    continue
                if part.get_content_type() == 'application/octet-stream':
                    attachmentsFolder = self.USER_MAILBOX + "Attachments/"
                    if not os.path.exists(attachmentsFolder):
                        os.mkdir(attachmentsFolder)
                    completePath = attachmentsFolder + part.get_filename()
                    with open(completePath, 'wb') as fp:
                        fp.write(part.get_payload(decode=True))

    def endSession(self):
        self.__command_QUIT()
        
    def __command_USER(self):
        userCommand = f"USER {self.username}\r\n"
        self.clientSocket.send(userCommand.encode())
        recv = self.clientSocket.recv(1024).decode()

    def __command_PASS(self):
        passCommand = f"PASS {self.password}\r\n"
        self.clientSocket.send(passCommand.encode())
        recv = self.clientSocket.recv(1024).decode()

    def __command_STAT(self):
        statCommand = "STAT\r\n"
        self.clientSocket.send(statCommand.encode())
        recv = self.clientSocket.recv(1024).decode()
        self.numberOfMails = recv.split()[1]

    def __command_LIST(self):
        listCommand = "LIST\r\n"
        self.clientSocket.send(listCommand.encode())
        recv = self.clientSocket.recv(1024).decode()

    def __command_RETR(self, mailNumber=1):
        self.msgID = remove_extension(self.serverMails[mailNumber - 1])
        recv = b""
        retrCommand = f"RETR {mailNumber}\r\n"
        self.clientSocket.send(retrCommand.encode())
        while True:
            chunk = self.clientSocket.recv(1024)
            if not chunk:
                break
            recv += chunk

        print(recv.decode())
        return recv

    def __command_RETR(self, mailNumber=1):
        self.msgID = remove_extension(self.serverMails[mailNumber - 1])
        recv = b""
        retrCommand = f"RETR {mailNumber}\r\n"
        self.clientSocket.send(retrCommand.encode())
        while True:
            try:
                chunk = self.clientSocket.recv(1024)
                if not chunk:
                    break
                recv += chunk
            except socket.timeout:
                break  # Break the loop if no data is received within the timeout
        return recv
    # def __command_QUIT(self):
    #     QUITcommand = "QUIT\r\n"
    #     self.clientSocket.send(QUITcommand.encode())
    #     self.clientSocket.recv(1024)

    def __command_QUIT(self):
        QUITcommand = "QUIT\r\n"
        self.clientSocket.send(QUITcommand.encode())
        self.clientSocket.close()

if __name__ == "__main__":
    pass