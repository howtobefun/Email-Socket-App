import flet as ft
import os
from email import message_from_string
from UI_User import *
from UI_Send import *

class InboxMailContainerComponent:
    def __init__(self, header: list, delete_mail: callable):
        super().__init__()
        self.header=header
        self.delete_mail = delete_mail

    def remove_mail_from_list(self, e):
        self.delete_mail(self)

    def build(self):
        return ft.Containerft.TextButton(
            content=ft.Row(
                [
                    ft.TextField(
                    value = self.header[0],
                    read_only=True,
                    label="From", border="none"
                ),
                ft.TextField(
                    value = self.header[1],
                    read_only=True,
                    label="Subject", border="none"
                )
                ],
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )

class InboxSetion(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.headers = getAllMailHeader()
        self.InboxSectionColumn = ft.Column()
        self.create_inbox_section()

    def delete_mail(self, mailContainerComponent: InboxMailContainerComponent):
        controlToDelete = self.findControlByPath(mailContainerComponent.header[2])
        if (controlToDelete == None):
            return
        self.headers.remove(mailContainerComponent.header)
        self.InboxSectionColumn.controls.remove(controlToDelete)
        del mailContainerComponent
        self.update()

    def create_inbox_section(self):
        for Header in self.headers:
            mailContainerComponent=InboxMailContainerComponent(Header, self.delete_mail)
            inboxMail = ft.TextButton(
                content=ft.Row(
                    [
                        ft.TextField(
                            value = Header[0],
                            read_only=True,
                            label="From", border="none",
                            width=60
                        ),
                        ft.TextField(
                            value = Header[1],
                            read_only=True,
                            label="Subject", border="none",
                            width=60
                        ),
                        ft.IconButton(
                            ft.icons.DELETE,
                            on_click= mailContainerComponent.remove_mail_from_list                        )
                    ],
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                key=Header[2]
            )
            self.InboxSectionColumn.controls.append(inboxMail)
            self.update()

    def build(self):
        return self.InboxSectionColumn

    def findControlByPath(self, path: str):
        for control in self.InboxSectionColumn.controls:
            if control.key == path:
                print(control.key)
                return control
        return None

def getAllMailHeader():
    user = User()
    USER_MAILBOX_PATH = user.POP3client.USER_MAILBOX_PATH
    res_header_list = []
    if not os.path.exists(USER_MAILBOX_PATH):
        return []
    
    msgFolders = os.listdir(USER_MAILBOX_PATH)
    for folder in msgFolders:
        dir = USER_MAILBOX_PATH + f"{folder}/"
        entries = os.listdir(dir)
        for entry in entries:
            files = [entry for entry in entries if os.path.isfile(os.path.join(dir, entry))]
            for file in files:
                with open(dir + file, 'r') as fp:
                    content = fp.read()
                    content = message_from_string(content)
                    res_header = [content['From'],content['Subject'], dir + file]
                res_header_list.append(res_header)

    return res_header_list

def MailClassify(name):
    return ft.TextField(value="dang chon "+name)

def HomePage(page: ft.Page):
    user = User()

    def dropdown_changed(e):
        nextMail=MailClassify(mailClass.value)
        curMail.value=nextMail.value
        page.update()

    mailClass = ft.Dropdown(
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("Mail received"),
            ft.dropdown.Option("Inbox"),
            ft.dropdown.Option("School"),
            ft.dropdown.Option("Work"),
            ft.dropdown.Option("Spam"),
        ],
        width=200,
        value="Mail received",
        autofocus=True
    )

    def ComposeNewMail(e):#e để nhận tín hiệu từ nút
        page.controls.pop()
        page.clean()
        SendPage(page)

    def retrieveAllMailsFromServer(e):
        user.POP3client.retrieveAllMails()

    curMail=MailClassify(mailClass.value)
    
    sentMail=ft.TextButton(
        text="Sent mail",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    trashCan=ft.TextButton(
        text="Trash can",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    composeMail=ft.TextButton(
        text="Compose Mail",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click= ComposeNewMail
    )

    retrieveMails=ft.TextButton(
        text="Retrieve all mails",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click= retrieveAllMailsFromServer
    )

    inboxSection = InboxSetion()

    ButtonSection = ft.Column(
        [
            mailClass,
            curMail,
            sentMail,
            trashCan, 
            composeMail,
            retrieveMails
        ]
    )
 
    page.add(
        ft.Row(
            [
                ButtonSection,
                inboxSection.InboxSectionColumn
            ],
            alignment=ft.MainAxisAlignment.START
        )
    )
   
   

if __name__ == "__main__":
    ft.app(target=HomePage)

     
     

    
