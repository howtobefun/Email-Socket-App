import socket
import os
from email import message_from_bytes
from email import message_from_string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        self.email_message = None

        self.msgFile = None
        self.msgID = None
        self.msgPath = None

        dir_path = os.path.join(SERVER_MAILBOX_PATH, username)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        self.serverMails = os.listdir(dir_path)

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
            self.retrieveMail(mailNumber=i)
            self.endSession()
        if (os.path.isdir(SERVER_MAILBOX_PATH + self.username)):
            os.rmdir(SERVER_MAILBOX_PATH + self.username)
    
    def retrieveMail(self, mailNumber=1):
        self.__retrieveMailMessage(mailNumber)
        self.__retrieveAttachments()
        os.remove(SERVER_MAILBOX_PATH + self.username + "/" + self.msgFile)
        if isEmpty(SERVER_MAILBOX_PATH + self.username):
            os.rmdir(SERVER_MAILBOX_PATH + self.username)

    def __connectWithServer(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.mailserver, self.port))
        self.clientSocket.settimeout(2)
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

        write_msg = MIMEMultipart()
        write_msg["From"] = self.email_message["From"]
        write_msg["To"] = self.email_message["To"]
        write_msg["Cc"] = self.email_message["Cc"]
        write_msg["Bcc"] = self.email_message["Bcc"]
        write_msg["Subject"] = self.email_message["Subject"]
        for part in self.email_message.walk():
            if part.get_content_type() == 'text/plain':
                write_msg.attach(MIMEText(part.get_payload()))
        with open(self.msgPath + self.msgFile, "w") as fp:
            fp.write(write_msg.as_string())
    
    def __retrieveAttachments(self):
        if self.email_message.is_multipart():
            for part in self.email_message.walk():
                if part.get_content_type() == 'text/plain':
                    continue
                if part.get_content_type() == 'application/octet-stream':
                    attachmentsFolder = self.msgPath + "Attachments/"
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
        if not os.path.exists(SERVER_MAILBOX_PATH + self.username):
            os.mkdir(SERVER_MAILBOX_PATH + self.username)
            if not os.path.exists(SERVER_MAILBOX_PATH + self.username + "/" + self.msgID):
                os.mkdir(SERVER_MAILBOX_PATH + self.username + "/" + self.msgID)
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
        self.msgFile = self.serverMails[mailNumber - 1]
        self.msgID = remove_extension(self.msgFile)
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

    def __command_QUIT(self):
        QUITcommand = "QUIT\r\n"
        self.clientSocket.send(QUITcommand.encode())
        self.clientSocket.close()

if __name__ == "__main__":
    pass