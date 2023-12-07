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
        self.filePicker = ft.FilePicker(on_result=self.addFile)
        self.fileBar = ft.Row()
        self.filePath=[]
        
       
    def build(self):
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
        if e.files == None:
            return
        fileOverSizePath=""
        for x in e.files:    
            if x.size < 1000000:
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
            else:
                if(fileOverSizePath==""):
                    fileOverSizePath=x.name
                else:
                    fileOverSizePath=fileOverSizePath+"\n"+x.name
    
        self.update()
        if(fileOverSizePath!=""):
            fileOverSizeAlertDialog=ft.AlertDialog(title=ft.Text("Can't send file > 1MB"),content=ft.Text(fileOverSizePath))
            self.page.dialog =fileOverSizeAlertDialog
            fileOverSizeAlertDialog.open=True
            self.page.update()
            


class SendPage(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.user = User()
        self.page=page
        
        self.to = ft.TextField(label="To",height=40, width=500)
        self.cc = ft.TextField(label="Cc", height=40,width=500)
        self.bcc = ft.TextField(label="Bcc", height=40, width=500)
        self.subject = ft.TextField(label="Subject", height=40,)
        self.content= ft.TextField(label="Content", min_lines=8, multiline=True, height=220)
        self.sendButton=ft.ElevatedButton(text="Send",on_click=self.send)
        self.sendingAnnounce=ft.Text(value="")
        self.file = PickFileSystem(self.page) 

    def send(self,e):
        if(self.to.value):
            self.user.SMTPclient.sendEmail(
                mailTo_str= self.to.value,
                cc_str= self.cc.value,
                bcc_str= self.bcc.value,
                subject= self.subject.value,
                content= self.content.value,
                attachments= ", ".join(self.file.filePath)
            )
            self.page.views[-1].controls.append(ft.Row([ft.Text(value="Sending successfully")],alignment=ft.MainAxisAlignment.CENTER))
            self.page.update()
            self.update()

    def build(self):
        return ft.Column(
            controls=[
                self.to,self.cc,self.bcc,
                self.subject,
                self.file,
                self.content,
                ft.Row([self.sendButton],alignment=ft.MainAxisAlignment.END),
            ],
            alignment=ft.MainAxisAlignment.START
            )