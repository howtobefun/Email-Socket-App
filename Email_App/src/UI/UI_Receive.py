import flet as ft
from email import message_from_file
from UI_User import *

class ReceivePage(ft.UserControl):
    def __init__(self,page,msg_dir):
        super().__init__()
        self.page=page

        self.msg_dir = msg_dir
        self.msg_file=self.msg_dir+self.getFileName()
        self.msg = self.getMSG()

        content = self.getContent()

        self.fromUser = ft.TextField(label="From", width=500, value=self.msg['From'])
        self.to = ft.TextField(label="To",height=40, width=500, value=self.msg['To'])
        self.cc = ft.TextField(label="Cc", height=40,width=500, value=self.msg['Cc'])
        self.bcc = ft.TextField(label="Bcc", height=40, width=500, value=self.msg['Bcc'])
        self.subject = ft.TextField(label="Subject", height=40, value=self.msg['Subject'])
        self.file=ft.Text(value="Received file:")
        self.content= ft.TextField(label="Content", min_lines=8, multiline=True, height=220, value=content)

    def getFileName(self):
        if self.msg_dir==None:
            return None
        dir_list=self.msg_dir.split("/")
        print(dir_list)
        return dir_list[2]+".msg"

    def getMSG(self):
        if (self.msg_file == None):
            return None
        with open(self.msg_file, 'r') as fp:
            msg = message_from_file(fp)
        return msg
    
    def getContent(self):
        if self.msg==None:
            return None
        for part in self.msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode()

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
