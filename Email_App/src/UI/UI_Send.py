import flet as ft
from UI_User import *


class PickFileSystem(ft.UserControl):
    def __init__(self, filePicker):
        super().__init__()
        self.filePicker = filePicker

    def build(self):
        self.fileBar = ft.Row("")
       # self.filePicker = ft.FilePicker(on_result=self.addFile)
        self.filePath=ft.Text("")
       # self.overlay.append(self.file_picker)

        return ft.Column(
            controls=[
                ft.ElevatedButton("Choose files",
                                on_click=lambda _: self.filePicker.pick_files(allow_multiple=True)),
                self.fileBar,     
            ]
        )
    
    def addFile(self,e: ft.FilePickerResultEvent):
        for x in e.files:    
            print(x.name)
            self.fileBar.controls.append(FileContainer(self.filePath,x.name))
            self.filePath.value = self.filePath.value+" "+x.path
            self.update()

class FileContainer(ft.UserControl):
    def __init__(self, filePath, fileName):
        super().__init__()
        self.filePath=filePath
        self.fileName = fileName

    def build(self):
        return ft.Container(
            content=ft.Row([
                            ft.Text(value=self.fileName),
                            ft.IconButton(
                                        ft.icons.DELETE,
                                        #on_click=deleteFile
                            )
                    ]
            ),
            bgcolor=ft.colors.BLUE_100
        )

       
    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

def SendPage(page: ft.Page):
    user = User()

    to = ft.TextField(label="To",height=40, width=500)
    cc = ft.TextField(label="Cc", height=40,width=500)
    bcc = ft.TextField(label="Bcc", height=40, width=500)
    subject = ft.TextField(label="Subject", height=40,)
    content= ft.TextField(label="Content", min_lines=12)

    def send(e):#e để nhận tín hiệu từ nút
        if(to.value):
            page.add(ft.Row([ft.Text(value="Sending successfully to "+ to.value,size=10)],
                            alignment=ft.MainAxisAlignment.CENTER))
            user.SMTPclient.sendEmail(
                mailTo_str= to.value,
                cc_str= cc.value,
                bcc_str= bcc.value,
                subject= subject.value,
                content= content.value,
                attachments= filePath.value
            )
    sendButton=ft.ElevatedButton(text="Send",on_click=send)


    fileBar=ft.Row()
    filePath=ft.Text("")

    def deleteFile(self,e):
        index=self.fileBar.index()
        del self.fileBar.controls



    def showPickFile(e: ft.FilePickerResultEvent):
        for x in e.files:    
            filePicked=ft.Container(
            content=ft.Row([ft.Text(value=x.name),
                            ft.IconButton(
                                ft.icons.DELETE,
                                on_click=deleteFile
                                )
                            ]
                        ),
            bgcolor=ft.colors.BLUE_100)
            fileBar.controls.append(filePicked)
            filePath.value = filePath.value+" "+x.path
            page.update()

    file_picker = ft.FilePicker(on_result=showPickFile)
    page.overlay.append(file_picker)
    
    p = PickFileSystem(file_picker) 


    # def doSomethingWithPickFile():
    #     if file_picker.result != None and file_picker.result.files != None:
    #         for f in file_picker.result.files:
    #             pass (tác động lên f)

    page.add(
          ft.Column(
            [
                to,cc,bcc,
                subject,
                # ft.ElevatedButton("Choose files",
                #     on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
                # fileBar,
                p,
                content
            ],
            alignment=ft.MainAxisAlignment.START
            ),
        ft.Row([sendButton],alignment=ft.MainAxisAlignment.END)
    )
     


if __name__ == "__main__":
    ft.app(target=SendPage)
