import flet as ft
from UI_User import *

def SendPage(page: ft.Page):
   # user = User()

    to = ft.TextField(label="To", width=500)
    cc = ft.TextField(label="Cc", multiline=True, width=500)
    bcc = ft.TextField(label="Bcc", multiline=True, width=500)
    subject = ft.TextField(label="Subject", multiline=True)
    content= ft.TextField(label="Content", multiline=True,min_lines=12)

    def send(e):#e để nhận tín hiệu từ nút
        if(to.value):
            page.add(ft.Row([ft.Text(value="Sending successfully to "+ to.value,size=10)],
                            alignment=ft.MainAxisAlignment.CENTER))
            # user.SMTPclient.sendEmail(
            #     mailTo_str= to.value,
            #     cc_str= cc.value,
            #     bcc_str= bcc.value,
            #     subject= subject.value,
            #     content= content.value
            # )
            

    sendButton=ft.ElevatedButton(text="Send",on_click=send)

    fname=" "
    fileName=ft.Text(value=fname)
    def showPickFile(e: ft.FilePickerResultEvent):
        for x in e.files:
            global fname
            fname=fname+x.name
            fileName.value=fname
            page.update()

    file_picker = ft.FilePicker(on_result=showPickFile)
    page.overlay.append(file_picker)


    page.add(
          ft.Column(
            [
               # to,cc,bcc,
                subject,
                ft.ElevatedButton("Choose files...",
                    on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
                fileName,
                content
            ],
            alignment=ft.MainAxisAlignment.START
            ),
        ft.Row([sendButton],alignment=ft.MainAxisAlignment.END)
    )
     
     

if __name__ == "__main__":
    ft.app(target=SendPage)
