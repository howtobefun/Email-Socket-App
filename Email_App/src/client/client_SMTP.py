import socket
import Mail

DEFAULT_SUBJECT = "Anh DuyTech"
DEFAULT_CONTENT = "Anh DuyTech"
DEFAULT_FILE_PATH = ""

class Client_SMTP:
    def __init__(self, mailserver, port, username, password, email):
        self.mailserver = mailserver
        self.port = port
        self.username = username
        self.email = email

        self.client_socket = None
        self.end_msg = "\r\n.\r\n"

    def connect_with_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.mailserver, self.port))
        recv = self.client_socket.recv(1024).decode()
        self._command_ehlo()

    def send_email(self, mail_to_str: str, cc_str: str, bcc_str: str, subject: str, content: str, attachments: str):
        mail_to = self.get_mail_to(mail_to_str)
        cc = self.get_cc(cc_str)
        bcc = self.get_bcc(bcc_str)

        for recipient in mail_to + cc:
            self.send_one_mail(recipient, mail_to, cc, "", subject, content, attachments)

        for recipient in bcc:
            self.send_one_mail(recipient, mail_to, cc, recipient, subject, content, attachments)

    def send_one_mail(self, recipient: str, mail_to: list, cc: list, bcc: str, subject: str, content: str, file_paths: str):
        mail = Mail.Mail(
            sender=self.email,
            mail_to=mail_to,
            cc=cc,
            bcc=bcc,
            subject=subject,
            content=content,
            file_paths=file_paths
        )
        self.connect_with_server()
        self._command_mail_from()
        self._command_rcpt_to(recipient)
        self._command_data(mail.get_mail_content())
        self.end_session()

    def get_mail_to(self, mail_to_str: str):
        if mail_to_str != "":
            mail_to = mail_to_str.split(Mail.COMMASPACE)
            return mail_to
        return []

    def get_cc(self, cc_str: str):
        if cc_str != "":
            cc = cc_str.split(Mail.COMMASPACE)
            return cc
        return []

    def get_bcc(self, bcc_str: str):
        if bcc_str != "":
            bcc = bcc_str.split(Mail.COMMASPACE)
            return bcc
        return []

    def end_session(self):
        self._command_quit()
        self.client_socket.close()

    def _command_ehlo(self):
        command = f'EHLO [{self.mailserver}]\r\n'
        self.client_socket.send(command.encode())
        recv = self.client_socket.recv(1024).decode()

    def _command_mail_from(self):
        command = f"MAIL FROM: <{self.username}>\r\n"
        self.client_socket.send(command.encode())
        recv = self.client_socket.recv(1024).decode()

    def _command_rcpt_to(self, recipient):
        command = f"RCPT TO: <{recipient}>\r\n"
        self.client_socket.send(command.encode())
        recv = self.client_socket.recv(1024).decode()

    def _command_data(self, msg):
        command = "DATA\r\n"
        self.client_socket.send(command.encode())
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] == '354':
            send_msg = msg + self.end_msg
            self.client_socket.send(send_msg.encode())
            self.client_socket.recv(1024)

    def _command_quit(self):
        command = "QUIT\r\n"
        self.client_socket.send(command.encode())
        self.client_socket.recv(1024)

if __name__ == "__main__":
    pass
