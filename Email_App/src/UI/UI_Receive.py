import flet as ft
from UI_User import *

def ReceivePage(page: ft.Page):
    SMTPclient = User().SMTPclient
    fromUser = ft.TextField(label="From", width=500)
    to = ft.TextField(label="To", width=500)
    cc = ft.TextField(label="Cc", multiline=True, width=500)
    bcc = ft.TextField(label="Bcc", multiline=True, width=500)
    subject = ft.TextField(label="Subject", multiline=True)
    content= ft.TextField(label="Content", multiline=True,min_lines=8)

    def reply(e):#e để nhận tín hiệu từ nút
        if(to.value):
            page.add(ft.Row([ft.Text(value="Sending successfully to "+ to.value,size=10)],
                            alignment=ft.MainAxisAlignment.CENTER))
            
            SMTPclient.sendEmail(
                mailTo_str= to.value,
                cc_str= cc.value,
                bcc_str= bcc.value,
                subject= subject.value,
                content= content.value
            )

    replyButton=ft.ElevatedButton(text="Reply",on_click=reply)
   
    page.add(
          ft.Column(
            [
                fromUser,
                to,cc,bcc,
                subject,
                content
            ],
            alignment=ft.MainAxisAlignment.START
            ),
        ft.Row([replyButton],alignment=ft.MainAxisAlignment.END)
    )
     
     

    
if __name__ == "__main__":
    ft.app(target=ReceivePage)
