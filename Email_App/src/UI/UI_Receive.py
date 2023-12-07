import flet as ft
from UI_User import *

class ReceivePage(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page=page
        #self.SMTPclient = User().SMTPclient

        self.fromUser = ft.TextField(label="From", width=500)
        self.to = ft.TextField(label="To",height=40, width=500)
        self.cc = ft.TextField(label="Cc", height=40,width=500)
        self.bcc = ft.TextField(label="Bcc", height=40, width=500)
        self.subject = ft.TextField(label="Subject", height=40,)
        self.file=ft.Text(value="Received file:")
        self.content= ft.TextField(label="Content", min_lines=8, multiline=True, height=220)


    def build(self):
        return ft.Column(
            controls=[
                self.fromUser,
                self.to,self.cc,self.bcc,
                self.subject,
                self.file,
                self.content,
            ],
            alignment=ft.MainAxisAlignment.START
            )
   
 
    
def ReceiveMain(page: ft.Page):
    page.add(ReceivePage(page))


if __name__ == "__main__":
    ft.app(target=ReceiveMain)
