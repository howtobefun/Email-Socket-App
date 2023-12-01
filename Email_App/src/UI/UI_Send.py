import flet as ft
from UI_User import *

class FileContainerComponent:
    def __init__(self, filePath: str, fileName: str, delete_file: callable):
        self.filePath = filePath
        self.fileName = fileName
        self.delete_file = delete_file
    def remove_file_from_list(self, e):
        self.delete_file(self)
   

class PickFileSystem(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page=page

    def build(self):
        self.fileBar = ft.Row()
        self.filePicker = ft.FilePicker(on_result=self.addFile)
        self.filePath=[]
        self.page.overlay.append(self.filePicker)

        return ft.Column(
            controls=[
                ft.ElevatedButton("Choose files",
                                on_click=lambda _: self.filePicker.pick_files(allow_multiple=True)),
                self.fileBar,     
            ]
        )
    
    def findControlByPath(self,path: str):
            for control in self.fileBar.controls:
                if control.key == path:
                    return control
            return None

    def deleteFile(self,fileContainerComponent: FileContainerComponent):
        controlToDelete = self.findControlByPath(fileContainerComponent.filePath)
        if (controlToDelete == None):
            return
        self.filePath.remove(fileContainerComponent.filePath)
        self.fileBar.controls.remove(controlToDelete)
        del fileContainerComponent
        self.update()

    def addFile(self,e: ft.FilePickerResultEvent):
        for x in e.files:    
            fileContainerComponent = FileContainerComponent(x.path, x.name, self.deleteFile)
            filePicked=ft.Container(
                            content=ft.Row(
                                        controls=[
                                            ft.Text(value=x.name),
                                            ft.IconButton(
                                                    ft.icons.DELETE,
                                                    on_click=fileContainerComponent.remove_file_from_list
                                            )
                                        ]
                            ),
                            bgcolor=ft.colors.BLUE_100,
                            key=x.path
            )
            self.fileBar.controls.append(filePicked)
            self.filePath.append(x.path)
            self.update()


def SendPage(page: ft.Page):
    user = User()

    to = ft.TextField(label="To",height=40, width=500)
    cc = ft.TextField(label="Cc", height=40,width=500)
    bcc = ft.TextField(label="Bcc", height=40, width=500)
    subject = ft.TextField(label="Subject", height=40,)
    content= ft.TextField(label="Content", min_lines=12)

    def send(e):
        if(to.value):
            page.add(ft.Row([ft.Text(value="Sending successfully to "+ to.value,size=10)],
                            alignment=ft.MainAxisAlignment.CENTER))
            user.SMTPclient.sendEmail(
                mailTo_str= to.value,
                cc_str= cc.value,
                bcc_str= bcc.value,
                subject= subject.value,
                content= content.value,
                attachments= ", ".join(file.filePath)
            )
    sendButton=ft.ElevatedButton(text="Send",on_click=send)
    
    file = PickFileSystem(page) 

    page.add(
          ft.Column(
            [
                to,cc,bcc,
                subject,
                file,
                content
            ],
            alignment=ft.MainAxisAlignment.START
            ),
        ft.Row([sendButton],alignment=ft.MainAxisAlignment.END)
    )
     


if __name__ == "__main__":
    ft.app(target=SendPage)
