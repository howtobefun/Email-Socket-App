import flet as ft
from client import *

def main(page: ft.Page):
    page.title = "Email Client"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width=800
    page.window_height=700
    page.window_resizable=False

    to = ft.TextField(label="To", width=500)
    cc =ft.TextField(
            label="Cc",
            multiline=True,
            min_lines=0,
           # height=60, 
            width=500
        )
    bcc =ft.TextField(
            label="Bcc",
            multiline=True,
            min_lines=0,
       #     height=60, 
            width=500
        )
    sendAddress=ft.Column([to,cc,bcc])
    subject = ft.TextField(
        label="Subject",
        multiline=True,
        min_lines=0,
        height=60
    )
    content = ft.Container(
        ft.TextField(label="Content", multiline=True,min_lines=0,height=300, border= "none"),
        height=300,
        padding=5,
        border=ft.border.all()
    )

    def send(e):#e để nhận tín hiệu từ nút
        if(to.value):
            page.add(ft.Row([ft.Text(value="Sending successfully to "+ to.value,size=10)],alignment=ft.MainAxisAlignment.CENTER))

    
    sendButton=ft.ElevatedButton(text="Send",on_click=send)
   
    page.add(
        ft.Column(
            [
                sendAddress,
                subject,
                content
            ],
            alignment=ft.MainAxisAlignment.START
            ),
        ft.Row([sendButton],alignment=ft.MainAxisAlignment.END)
     )
    
if __name__ == "__main__":
    username = sender
    password = "password"

    SMTPclient = Client_SMTP(mailserver, SMTPport, username)
    ft.app(target=main)