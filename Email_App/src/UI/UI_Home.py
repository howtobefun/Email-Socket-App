import flet as ft
import os
import shutil
from email import message_from_string
from Filter import *
from UI_Send import *
from UI_User import *

def get_all_mail_header(mail_class: str):#tui thêm mail class 
    user = User()
    MAIL_CLASS_FOLDER = user.pop3_client.USER_MAILBOX_PATH + mail_class + "/"
    res_header_list = []
    if not os.path.exists(MAIL_CLASS_FOLDER):
        return []

    msg_folders = os.listdir(MAIL_CLASS_FOLDER)
    for folder in msg_folders:
        dir = MAIL_CLASS_FOLDER + f"{folder}/"
        entries = os.listdir(dir)
        files = [entry for entry in entries if os.path.isfile(os.path.join(dir, entry))]
        for file in files:
            with open(dir + file, 'r') as fp:
                content = fp.read()
                content = message_from_string(content)
                res_header = [content['From'], content['Subject'], dir]
            res_header_list.append(res_header)
            
    return res_header_list

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

    def change_class(self, class_change: str):  # hàm đổi inbox section, tui đang ko biết có nên gộp 2 hàm change_class với create_inbox_section lại làm 1 ko
        self.inbox_section_column.controls.clear()
        self.mail_class=class_change
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
        self.update()

class UserInformation(ft.UserControl):
    def __init__(self, page, user:User):
        super().__init__()
        self.user = user
        self.page = page

        self.user_name=ft.Text(value=self.user.pop3_client.username,weight='bold')
        self.user_email=ft.Text(value="<"+self.user.pop3_client.email+">")
        self.user_avatar=ft.CircleAvatar(
                    content=ft.Text(self.get_initials(self.user.pop3_client.username)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(self.user.pop3_client.username),
                    radius=25
        )
        
    def get_initials(self, user_name: str):
        return user_name[0].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
    
    def build(self):
        return ft.Row(
            [
                self.user_avatar,
                ft.Column(
                    [
                        self.user_name,
                        self.user_email
                    ]
                )
            ]
        )

class HomePage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.user = User()
        self.filter_utility = Filter() 
        self.page = page
        
        self.user_information=UserInformation(page=self.page,user=self.user)
        self.mail_filter = ft.Dropdown(  # lấy tên filter = self.mail_filter.value
            on_change=self.dropdown_changed,
            options=[
                ft.dropdown.Option("Inbox"),
                ft.dropdown.Option("School"),
                ft.dropdown.Option("Work"),
                ft.dropdown.Option("Spam"),
            ],
            width=200,
            value="Inbox",
            autofocus=True
        )

        self.inbox_section = InboxSection(self.mail_filter.value)

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
                self.user_information,
                self.mail_filter,
                self.compose_mail,
                self.retrieve_mails,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.MainAxisAlignment.CENTER
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
        self.inbox_section.change_class(self.mail_filter.value)
        self.update()

    def compose_new_mail(self, e):
        self.page.go("/Compose")

    def retrieve_all_mails_from_server(self, e):
        self.user.pop3_client.retrieve_all_mails()
        self.filter_utility.filter_all_mails()
        self.inbox_section.inbox_section_column.clean()
        self.inbox_section.create_inbox_section()
        self.inbox_section.update()

        self.show_announcement("Retrieved successfully")

    def show_announcement(self, announcement: str):
        announce_dialog = ft.AlertDialog(
            content=ft.Text(value=announcement),
            content_padding=ft.padding.all(20)
        )
        self.page.dialog = announce_dialog
        announce_dialog.open = True
        self.page.update()


def home_main(page: ft.Page):
    page.add(HomePage(page))


if __name__ == "__main__":
    ft.app(target=home_main)
