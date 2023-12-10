import flet as ft
import os
import shutil
from email import message_from_string
from UI_Send import *
from UI_User import *

def get_all_mail_header(mail_class: str):
    user = User()
    USER_MAILBOX_PATH = user.POP3client.USER_MAILBOX_PATH + mail_class + "/"
    print(USER_MAILBOX_PATH)
    res_header_list = []
    if not os.path.exists(USER_MAILBOX_PATH):
        return []

    msg_folders = os.listdir(USER_MAILBOX_PATH)
    for folder in msg_folders:
        dir = USER_MAILBOX_PATH + f"{folder}/"
        entries = os.listdir(dir)
        files = [entry for entry in entries if os.path.isfile(os.path.join(dir, entry))]
        for file in files:
            with open(dir + file, 'r') as fp:
                content = fp.read()
                content = message_from_string(content)
                res_header = [content['From'], content['Subject'], dir]
            res_header_list.append(res_header)

    return res_header_list

def download_all_attachments():
    user = User()
    USER_MAILBOX_PATH = user.POP3client.USER_MAILBOX_PATH
    res_header_list = []
    if not os.path.exists(USER_MAILBOX_PATH):
        return []

    msg_folders = os.listdir(USER_MAILBOX_PATH)
    for folder in msg_folders:
        dir = USER_MAILBOX_PATH + f"{folder}/"
        entries = os.listdir(dir)
        files = [entry for entry in entries if os.path.isfile(os.path.join(dir, entry))]
        for file in files:
            with open(dir + file, 'r') as fp:
                content = fp.read()
                content = message_from_string(content)

            for part in content.walk():
                if part.get_content_type() == 'text/plain':
                    continue
                if part.get_content_type() == 'application/octet-stream':
                    attachments_folder = dir + "Attachments/"
                    if not os.path.exists(attachments_folder):
                        os.mkdir(attachments_folder)
                    complete_path = attachments_folder + part.get_filename()
                    with open(complete_path, 'wb') as fp:
                        fp.write(part.get_payload(decode=True))

class InboxMailContainerComponent:
    def __init__(self, header: list, delete_mail: callable, check_receive_mail: callable):
        super().__init__()
        self.header = header
        self.delete_mail = delete_mail
        self.routing_utility = RoutingUtility(self.header[2], check_receive_mail)

    def remove_mail_from_list(self, e):
        self.delete_mail(self)

class RoutingUtility:
    def __init__(self, path: str, go: callable):
        self.go = go
        self.path = path

    def go_to_receive_page(self, e):
        self.go(self.path)

class InboxSection(ft.UserControl):
    def __init__(self, mail_class: str):
        super().__init__()
        self.mail_class = mail_class
        self.headers = get_all_mail_header(self.mail_class)
        self.inbox_section_column = ft.Column()
        self.create_inbox_section()

    def delete_mail(self, mail_container_component: InboxMailContainerComponent):
        control_to_delete = self.find_control_by_path(mail_container_component.header[2])
        if control_to_delete is None:
            return
        shutil.rmtree(mail_container_component.header[2])
        self.headers.remove(mail_container_component.header)
        self.inbox_section_column.controls.remove(control_to_delete)
        del mail_container_component
        self.update()

    def check_receive_mail(self, path: str):
        self.page.go(f"/Receive, {path}")

    def create_inbox_section(self):
        self.headers = get_all_mail_header(self.mail_class)
        for header in self.headers:
            mail_container_component = InboxMailContainerComponent(header, self.delete_mail, self.check_receive_mail)
            inbox_mail = ft.TextButton(
                content=ft.Row(
                    [
                        ft.TextField(
                            value=header[0],
                            read_only=True,
                            label="From", border="none",
                            width=60
                        ),
                        ft.TextField(
                            value=header[1],
                            read_only=True,
                            label="Subject", border="none",
                            width=60
                        ),
                        ft.IconButton(
                            ft.icons.DELETE,
                            on_click=mail_container_component.remove_mail_from_list
                        )
                    ],
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                key=header[2],  # path to mail
                on_click=mail_container_component.routing_utility.go_to_receive_page
            )
            self.inbox_section_column.controls.append(inbox_mail)

    def build(self):
        return self.inbox_section_column

    def find_control_by_path(self, path: str):
        for control in self.inbox_section_column.controls:
            if control.key == path:
                return control
        return None

    def change_class(self, class_change: str):  # hàm đổi inbox section
        self.inbox_section_column.controls.clear()
        self.headers = get_all_mail_header(class_change)
        for header in self.headers:
            mail_container_component = InboxMailContainerComponent(header, self.delete_mail, self.check_receive_mail)
            inbox_mail = ft.TextButton(
                content=ft.Row(
                    [
                        ft.TextField(
                            value=header[0],
                            read_only=True,
                            label="From", border="none",
                            width=60
                        ),
                        ft.TextField(
                            value=header[1],
                            read_only=True,
                            label="Subject", border="none",
                            width=60
                        ),
                        ft.IconButton(
                            ft.icons.DELETE,
                            on_click=mail_container_component.remove_mail_from_list
                        )
                    ],
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                key=header[2],  # path to mail
                on_click=mail_container_component.routing_utility.go_to_receive_page
            )
            self.inbox_section_column.controls.append(inbox_mail)
        self.update()


class HomePage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.user = User()
        self.page = page

        self.mail_filter = ft.Dropdown(  # lấy tên filter = self.mail_filter.value
            on_change=self.dropdown_changed,
            options=[
                ft.dropdown.Option("Mail_Received"),
                ft.dropdown.Option("Inbox"),
                ft.dropdown.Option("School"),
                ft.dropdown.Option("Work"),
                ft.dropdown.Option("Spam"),
            ],
            width=200,
            value="Mail_Received",
            autofocus=True
        )

        self.inbox_section = InboxSection(self.mail_filter.value)

        self.cur_mail = self.mail_classify(self.mail_filter.value)

        self.dowload_button = ft.TextButton(
            text="Download All",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=self.download_all_mail
        )
        self.compose_mail = ft.TextButton(
            text="Compose Mail",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=self.compose_new_mail
        )
        self.retrieve_mails = ft.TextButton(
            text="Retrieve All Mails",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=self.retrieve_all_mails_from_server
        )

    def build(self):
        self.button_section = ft.Column(
            [
                self.mail_filter,
                self.cur_mail,
                self.dowload_button,
                self.compose_mail,
                self.retrieve_mails,
            ],
            alignment=ft.MainAxisAlignment.START
        )
        return ft.Row(
            controls=[
                self.button_section,
                self.inbox_section
            ],
        )

    def mail_classify(self, name):
        return ft.TextField(value="dang chon " + name)

    def dropdown_changed(self, e):
        self.cur_mail.value = self.mail_classify(self.mail_filter.value).value
        self.inbox_section.change_class(self.mail_filter.value)
        self.update()

    def compose_new_mail(self, e):
        self.page.go("/Compose")

    def retrieve_all_mails_from_server(self, e):
        self.user.POP3client.retrieve_all_mails()
        self.inbox_section.inbox_section_column.clean()
        self.inbox_section.create_inbox_section()
        self.inbox_section.update()

        self.show_announcement("Retrieve successfully")

    def download_all_mail(self, e):
        # do something
        self.show_announcement("Download successfully")

    def show_announcement(self, announcement: str):
        announce_dialog = ft.AlertDialog(content=ft.Text(value=announcement),
                                         content_padding=ft.padding.all(20)
                                         )
        self.page.dialog = announce_dialog
        announce_dialog.open = True
        self.page.update()


def home_main(page: ft.Page):
    page.add(HomePage(page))


if __name__ == "__main__":
    ft.app(target=home_main)
