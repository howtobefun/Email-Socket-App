import flet as ft
from UI_User import *
from UI_Send import *

class InboxMail(ft.UserControl):
    def __init__(self, header):
        super().__init__()
        self.page=header

    def build(self):
        return ft.TextButton(
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

# class InboxSetion(ft.UserControl):
#     def __init__(self, user:User()):
#         super().__init__()
#         self.user=user
#         self.inboxSection=ft.Row()
#         self.USER_MAIL_BOX = MAILBOX_PATH + user.POP3client.username + "/"

#     def build(self):
#         for x
#             header= self.user.POP3client.getMailHeader()
#             inboxMail=InboxMail(header)
#             self.inboxSection.controls.append(inboxMail)
#         return self.inbox

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

    USER_MAIL_BOX = user.POP3client.USER_MAILBOX_PATH + user.POP3client.username + "/"
    Headers = user.POP3client.getAllMailHeader()

    InboxSection = ft.Column()

    for Header in Headers:
        inboxMail = ft.TextButton(
            content=ft.Row(
                [
                    ft.TextField(
                        value = Header[0],
                        read_only=True,
                        label="From", border="none"
                    ),
                    ft.TextField(
                        value = Header[1],
                        read_only=True,
                        label="Subject", border="none"
                    )
                ],
            ),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )
        InboxSection.controls.append(inboxMail)
        page.update()

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
                InboxSection
            ],
            alignment=ft.MainAxisAlignment.START
        )
    )
   
   

if __name__ == "__main__":
    ft.app(target=HomePage)

     
     

    
