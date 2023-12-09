import flet as ft
from email import message_from_file
from UI_User import *

class ReceivePage(ft.UserControl):
    def __init__(self,page,**kwargs):
        super().__init__()
        self.page=page

        self.msg_dir = kwargs.get('msg_dir', None)
        self.msg = self.getMsg()

        self.fromUser = ft.TextField(label="From", width=500, value=self.msg['From'])
        self.to = ft.TextField(label="To",height=40, width=500, value=self.msg['To'])
        self.cc = ft.TextField(label="Cc", height=40,width=500, value=self.msg['Cc'])
        self.bcc = ft.TextField(label="Bcc", height=40, width=500, value=self.msg['Bcc'])
        self.subject = ft.TextField(label="Subject", height=40, value=self.msg['Subject'])
        self.file=ft.Text(value="Received file:")
        self.content= ft.TextField(label="Content", min_lines=8, multiline=True, height=220, value=self.msg.get_payload())

    def getMSG(self):
        if (self.msg_dir == None):
            return None
        with open(self.msg_dir, 'rb') as fp:
            msg = message_from_file(fp)
        return msg

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
