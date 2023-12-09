import flet as ft
import os
import shutil
from email import message_from_string
from UI_User import *
from UI_Send import *

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

def download_all_attachments():
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
            
            for part in content.walk():
                if part.get_content_type() == 'text/plain':
                    continue
                if part.get_content_type() == 'application/octet-stream':
                    attachmentsFolder = dir + "Attachments/"
                    if not os.path.exists(attachmentsFolder):
                        os.mkdir(attachmentsFolder)
                    completePath = attachmentsFolder + part.get_filename()
                    with open(completePath, 'wb') as fp:
                        fp.write(part.get_payload(decode=True))

class InboxMailContainerComponent:
    def __init__(self, header: list, delete_mail: callable):
        super().__init__()
        self.header=header
        self.delete_mail = delete_mail

    def remove_mail_from_list(self, e):
        self.delete_mail(self)


class InboxSection(ft.UserControl):
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
            def checkReceiveMail(e):
                #do something to load information of received mail
                self.page.go(
                    route='/Receive', 
                    kwargs={
                        'msg_dir': inboxMail.key
                    } #the page will go if remove the args
                )
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
                            on_click= mailContainerComponent.remove_mail_from_list
                        )
                    ],
                ),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                key=Header[2], #path to mail
                on_click=checkReceiveMail
            )
            self.InboxSectionColumn.controls.append(inboxMail)

    def build(self):
        return self.InboxSectionColumn

    def findControlByPath(self, path: str):
        for control in self.InboxSectionColumn.controls:
            if control.key == path:
                return control
        return None

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

        self.inboxSection = InboxSection()        
        self.curMail=self.MailClassify(self.mailFilter.value)
        self.dowloadButton=ft.TextButton(
            text="Dowload All",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=self.downloadAllMail
        )
        self.composeMail=ft.TextButton(
            text="Compose Mail",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=self.composeNewMail
        )
        self.retrieveMails=ft.TextButton(
            text="Retrieve All Mails",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click= self.retrieveAllMailsFromServer
        )
        
    def build(self):
        self.ButtonSection = ft.Column(
            [
                self.mailFilter,
                self.curMail,   
                self.dowloadButton, 
                self.composeMail,
                self.retrieveMails,
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

    def composeNewMail(self,e):
        self.page.go("/Compose")

    def retrieveAllMailsFromServer(self,e):
        self.user.POP3client.retrieveAllMails()
        self.inboxSection.InboxSectionColumn.clean()
        self.inboxSection.create_inbox_section()
        self.inboxSection.update()

        self.showAnnouncement("Retrieve successfully")

    def downloadAllMail(self,e):
        #do something
        self.showAnnouncement("Download successfully")

    def showAnnouncement(self,announcement:str):
        annouceDialog=ft.AlertDialog(content=ft.Text(value=announcement),
                                     content_padding=ft.padding.all(20)
                                    )
        self.page.dialog =annouceDialog
        annouceDialog.open=True
        self.page.update()

def HomeMain(page: ft.Page):
    page.add(HomePage(page))


if __name__ == "__main__":
    ft.app(target=HomeMain)