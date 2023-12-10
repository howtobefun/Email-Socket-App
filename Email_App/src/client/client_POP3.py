import socket
import os
import shutil
from email import message_from_bytes

SERVER_MAILBOX_PATH = "../Test_Server/"

def isEmpty(path): 
    if os.path.exists(path) and not os.path.isfile(path): 
        return not os.listdir(path)
    else: 
        return False

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
        self.totalSize = None
        self.email_message = None

        self.msgFile = None
        self.msgID = None
        self.msgPath = None

        self.SERVER_USER_PATH = os.path.join(SERVER_MAILBOX_PATH, username)
        self.serverMails = None

        self.USERS_MAILBOX = "User_Mailbox/"
        self.USER_MAILBOX_PATH = self.USERS_MAILBOX + self.username + "/"

    def showNumberOfMails(self):
        self.__connectWithServer()
        self.__command_STAT()
        self.endSession()

    def showListMails(self):
        self.__connectWithServer()
        self.__command_LIST()
        self.endSession()

    def retrieveAllMails(self):
        self.__connectWithServer()
        self.__command_STAT() # Get number of mails
        self.endSession()

        if (self.numberOfMails == None):
            return
        for i in range(1, int(self.numberOfMails) + 1):
            self.__connectWithServer()
            self.retrieveMail()
            self.endSession()
        if (os.path.isdir(SERVER_MAILBOX_PATH + self.username)):
            shutil.rmtree(SERVER_MAILBOX_PATH + self.username)
    
    def retrieveMail(self, mailNumber=1):
        self.serverMails = os.listdir(self.SERVER_USER_PATH)
        self.__retrieveMailMessage(mailNumber)
        self.__command_DELE(mailNumber)
        #os.remove(SERVER_MAILBOX_PATH + self.username + "/" + self.msgFile)

    def __connectWithServer(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.mailserver, self.port))
        recv = self.clientSocket.recv(1024).decode()
        self.__command_USER()
        self.__command_PASS()

    def __retrieveMailMessage(self, mailNumber=1):
        self.recvData = self.__command_RETR(mailNumber=mailNumber)
        recv_message = self.recvData[(self.recvData.find("\r\n".encode()) + 2):]
        self.email_message = message_from_bytes(recv_message)
        self.__transferMailMessageToMailBox()

    def __transferMailMessageToMailBox(self):
        self.msgPath = self.USER_MAILBOX_PATH + self.msgID + "/"
        if not os.path.exists(self.USER_MAILBOX_PATH):
            os.mkdir(self.USER_MAILBOX_PATH)
        if not os.path.exists(self.msgPath):
            os.mkdir(self.msgPath)

        with open(self.msgPath + self.msgFile, "w") as fp:
            fp.write(self.email_message.as_string())
    
    def __retrieveAttachments(self): # Save attachments to Attachments folder, use the logic later in UI
        if self.email_message.is_multipart():
            for part in self.email_message.walk():
                if part.get_content_type() == 'text/plain':
                    continue
                if part.get_content_type() == 'application/octet-stream':
                    attachmentsFolder = self.USER_MAILBOX_PATH + "Attachments/"
                    if not os.path.exists(attachmentsFolder):
                        os.mkdir(attachmentsFolder)
                    completePath = attachmentsFolder + part.get_filename()
                    if not os.path.isdir(completePath):
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
        self.totalSize = int(recv.split()[2])

    def __command_LIST(self):
        listCommand = "LIST\r\n"
        self.clientSocket.send(listCommand.encode())
        recv = self.clientSocket.recv(1024).decode()

    def __command_RETR(self, mailNumber=1):
        self.msgFile = self.serverMails[mailNumber - 1]
        self.msgID = remove_extension(self.msgFile)
        if not os.path.exists(SERVER_MAILBOX_PATH + self.username):
            os.mkdir(SERVER_MAILBOX_PATH + self.username)
            if not os.path.exists(SERVER_MAILBOX_PATH + self.username + "/" + self.msgID):
                os.mkdir(SERVER_MAILBOX_PATH + self.username + "/" + self.msgID)
        recv = b""
        retrCommand = f"RETR {mailNumber}\r\n"
        self.clientSocket.send(retrCommand.encode())
        recv = self.clientSocket.recv(self.totalSize + 10)

        return recv

    def __command_DELE(self, mailNumber=1):
        deleCommand = f"DELE {mailNumber}\r\n"
        self.clientSocket.send(deleCommand.encode())
        recv = self.clientSocket.recv(1024).decode()

    def __command_QUIT(self):
        QUITcommand = "QUIT\r\n"
        self.clientSocket.send(QUITcommand.encode())
        self.clientSocket.close()

if __name__ == "__main__":
    pass