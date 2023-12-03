import flet as ft
import os
import shutil
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
        shutil.rmtree(mailContainerComponent.header[2])
        self.headers.remove(mailContainerComponent.header)
        self.InboxSectionColumn.controls.remove(controlToDelete)
        del mailContainerComponent
        self.update()

    def create_inbox_section(self):
        self.headers = getAllMailHeader()
        for Header in self.headers:
            print(Header)
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
                            on_click= mailContainerComponent.remove_mail_from_list)
                    ],
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                key=Header[2]
            )
            self.InboxSectionColumn.controls.append(inboxMail)

    def build(self):
        return self.InboxSectionColumn

    def findControlByPath(self, path: str):
        for control in self.InboxSectionColumn.controls:
            if control.key == path:
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
        files = [entry for entry in entries if os.path.isfile(os.path.join(dir, entry))]
        for file in files:
            with open(dir + file, 'r') as fp:
                content = fp.read()
                content = message_from_string(content)
                res_header = [content['From'],content['Subject'], dir]
            res_header_list.append(res_header)

    return res_header_list


class HomePage(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.user=User()
        self.page=page

        self.mailFilter = ft.Dropdown(
            on_change=self.dropdown_changed,
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

        self.inboxSection = InboxSetion()        
        self.curMail=self.MailClassify(self.mailFilter.value)
        self.sentMail=ft.TextButton(
            text="Sent mail",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )
        self.trashCan=ft.TextButton(
            text="Trash can",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )
        self.composeMail=ft.TextButton(
            text="Compose Mail",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click= self.ComposeNewMail
        )
        self.retrieveMails=ft.TextButton(
            text="Retrieve all mails",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click= self.retrieveAllMailsFromServer
        )
        
    def build(self):
        self.ButtonSection = ft.Column(
            [
                self.mailFilter,
                self.curMail,
                self.sentMail,
                self.trashCan, 
                self.composeMail,
                self.retrieveMails
            ],
            alignment=ft.MainAxisAlignment.START
        )
        return ft.Row(
            controls=[
                self.ButtonSection,
                self.inboxSection
            ],
        )  
        
    def MailClassify(self,name):
        return ft.TextField(value="dang chon "+name)

    def dropdown_changed(self,e):
        self.curMail.value=self.MailClassify(self.mailFilter.value).value
        self.update()

    def ComposeNewMail(self,e):
        self.page.controls.pop()
        self.page.clean()
        self.page.add(SendPage(self.page))

    def retrieveAllMailsFromServer(self,e):
        self.user.POP3client.retrieveAllMails()
        self.inboxSection.InboxSectionColumn.clean()
        self.inboxSection.create_inbox_section()
        self.inboxSection.update()

   


def HomeMain(page: ft.Page):
    page.add(HomePage(page))


if __name__ == "__main__":
    ft.app(target=HomeMain)

     
     

    
