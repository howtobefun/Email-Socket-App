import flet as ft
from email import message_from_file
import os
from email import message_from_string
from UI_User import *

class ReceivePage(ft.UserControl):
    def __init__(self, page, msg_dir):
        super().__init__()
        self.page = page

        self.msg_dir = msg_dir
        # self.folder_dir = os.path.dirname(self.msg_dir) currently not used
        self.msg_file = self.msg_dir + self.get_file_name()
        self.msg = self.get_msg()

        content = self.get_content()

        self.from_sender = ft.TextField(label="From", height=40, expand=True, value=self.msg['From'], read_only=True)
        self.to = ft.TextField(label="To", height=40, value=self.msg['To'], read_only=True)
        self.cc = ft.TextField(label="Cc", height=40, value=self.msg['Cc'], read_only=True)
        self.bcc = ft.TextField(label="Bcc", height=40, value=self.msg['Bcc'], read_only=True)
        self.subject = ft.TextField(label="Subject", height=40, value=self.msg['Subject'], read_only=True)
        self.file = ft.Text(value="Received file:")
        self.content = ft.TextField(label="Content", min_lines=8, multiline=True, height=250, value=content,
                                    read_only=True)
        self.download_button = ft.IconButton(ft.icons.DOWNLOAD_ROUNDED, tooltip="Download Mail", on_click=self.download)

    def download(self, e):
        self.__download_all_attachments()
        self.show_announcement("Downloaded successfully")

    def get_file_name(self):
        if self.msg_dir is None:
            return None
        dir_list = self.msg_dir.split("/")
        return dir_list[3]

    def get_msg(self):
        if self.msg_file is None:
            return None
        with open(self.msg_file, 'r') as fp:
            msg = message_from_file(fp)
        return msg

    def get_content(self):
        if self.msg is None:
            return None
        for part in self.msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode()

    def build(self):
        return ft.Column(
            controls=[
                ft.Row([self.from_sender, self.download_button]),
                self.to, self.cc, self.bcc,
                self.subject,
                self.file,
                self.content,
            ],
            alignment=ft.MainAxisAlignment.START
        )
    
    def __download_all_attachments(self):
        user = User()
        attachments_folder = user.pop3_client.USER_MAILBOX_PATH + "Attachments/"
        with open(self.msg_file, 'r') as fp:
            content = fp.read()
            content = message_from_string(content)

        for part in content.walk():
            if part.get_content_type() == 'text/plain':
                continue
            if part.get_content_type() == 'application/octet-stream':
                if not os.path.exists(attachments_folder):
                    os.mkdir(attachments_folder)
                complete_path = attachments_folder + part.get_filename()
                with open(complete_path, 'wb') as fp:
                    fp.write(part.get_payload(decode=True))
    
    def show_announcement(self, announcement: str):
        announce_dialog = ft.AlertDialog(
            content=ft.Text(value=announcement),
            content_padding=ft.padding.all(20)
        )
        self.page.dialog = announce_dialog
        announce_dialog.open = True
        self.page.update()

def receive_main(page: ft.Page):
    page.add(ReceivePage(page))


if __name__ == "__main__":
    ft.app(target=receive_main)
