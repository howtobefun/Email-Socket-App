import socket
import os
import shutil
from email import message_from_bytes

SERVER_MAILBOX_PATH = "../Test_Server/"

def is_empty(path): 
    if os.path.exists(path) and not os.path.isfile(path): 
        return not os.listdir(path)
    else: 
        return False

def remove_extension(file_path):
        root, extension = os.path.splitext(file_path)
        return root

class Client_POP3:
    def __init__(self, mailserver, port, username, password, email):
        self.mailserver = mailserver
        self.port = port
        self.client_socket = None

        self.username = username
        self.password = password
        self.email = email

        self.number_of_mails = None

        self.recv_data = None
        self.total_size = None
        self.email_message = None

        self.msg_file = None
        self.msg_id = None
        self.msg_path = None

        self.SERVER_USER_PATH = os.path.join(SERVER_MAILBOX_PATH, self.email)
        self.server_mails = None

        self.USERS_MAILBOX = "User_Mailbox/"
        self.USER_MAILBOX_PATH = self.USERS_MAILBOX + self.email + "/"

    def show_number_of_mails(self):
        self.__connect_with_server()
        self.__command_stat()
        self.end_session()

    def show_list_mails(self):
        self.__connect_with_server()
        self.__command_list()
        self.end_session()

    def retrieve_all_mails(self):
        self.__connect_with_server()
        self.__command_stat()  # Get number of mails
        self.end_session()

        if self.number_of_mails is None:
            return
        for i in range(1, int(self.number_of_mails) + 1):
            self.__connect_with_server()
            self.retrieve_mail()
            self.end_session()
        if os.path.isdir(SERVER_MAILBOX_PATH + self.email):
            shutil.rmtree(SERVER_MAILBOX_PATH + self.email)

    def retrieve_mail(self, mail_number=1):
        self.server_mails = os.listdir(self.SERVER_USER_PATH)
        self.__retrieve_mail_message(mail_number)
        self.__command_dele(mail_number)

    def __connect_with_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.mailserver, self.port))
        recv = self.client_socket.recv(1024).decode()
        self.__command_user()
        self.__command_pass()

    def __retrieve_mail_message(self, mail_number=1):
        self.recv_data = self.__command_retr(mail_number=mail_number)
        recv_message = self.recv_data[(self.recv_data.find("\r\n".encode()) + 2):]
        self.email_message = message_from_bytes(recv_message)
        self.__transfer_mail_message_to_mailbox()

    def __transfer_mail_message_to_mailbox(self):
        self.msg_path = os.path.join(self.USER_MAILBOX_PATH, self.msg_id)
        if not os.path.exists(self.USER_MAILBOX_PATH):
            os.mkdir(self.USER_MAILBOX_PATH)
        if not os.path.exists(self.msg_path):
            os.mkdir(self.msg_path)

        with open(os.path.join(self.msg_path, self.msg_file), "w") as fp:
            fp.write(self.email_message.as_string())

    def __retrieve_attachments(self):  # Save attachments to Attachments folder, use the logic later in UI
        if self.email_message.is_multipart():
            for part in self.email_message.walk():
                if part.get_content_type() == 'text/plain':
                    continue
                if part.get_content_type() == 'application/octet-stream':
                    attachments_folder = os.path.join(self.USER_MAILBOX_PATH, "Attachments")
                    if not os.path.exists(attachments_folder):
                        os.mkdir(attachments_folder)
                    complete_path = os.path.join(attachments_folder, part.get_filename())
                    if not os.path.isdir(complete_path):
                        with open(complete_path, 'wb') as fp:
                            fp.write(part.get_payload(decode=True))

    def end_session(self):
        self.__command_quit()

    def __command_user(self):
        user_command = f"USER {self.email}\r\n"
        self.client_socket.send(user_command.encode())
        recv = self.client_socket.recv(1024).decode()

    def __command_pass(self):
        pass_command = f"PASS {self.password}\r\n"
        self.client_socket.send(pass_command.encode())
        recv = self.client_socket.recv(1024).decode()

    def __command_stat(self):
        stat_command = "STAT\r\n"
        self.client_socket.send(stat_command.encode())
        recv = self.client_socket.recv(1024).decode()
        self.number_of_mails = recv.split()[1]
        self.total_size = int(recv.split()[2])

    def __command_list(self):
        list_command = "LIST\r\n"
        self.client_socket.send(list_command.encode())
        recv = self.client_socket.recv(1024).decode()

    def __command_retr(self, mail_number=1):
        self.msg_file = self.server_mails[mail_number - 1]
        self.msg_id = remove_extension(self.msg_file)
        if not os.path.exists(os.path.join(SERVER_MAILBOX_PATH, self.email)):
            os.mkdir(os.path.join(SERVER_MAILBOX_PATH, self.email))
            if not os.path.exists(os.path.join(SERVER_MAILBOX_PATH, self.email, self.msg_id)):
                os.mkdir(os.path.join(SERVER_MAILBOX_PATH, self.email, self.msg_id))
        recv = b""
        retr_command = f"RETR {mail_number}\r\n"
        self.client_socket.send(retr_command.encode())
        recv = self.client_socket.recv(self.total_size + 10)

        return recv

    def __command_dele(self, mail_number=1):
        dele_command = f"DELE {mail_number}\r\n"
        self.client_socket.send(dele_command.encode())
        recv = self.client_socket.recv(1024).decode()

    def __command_quit(self):
        quit_command = "QUIT\r\n"
        self.client_socket.send(quit_command.encode())
        self.client_socket.close()

if __name__ == "__main__":
    pass
