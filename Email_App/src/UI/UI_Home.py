import flet as ft
from UI_User import *
from UI_Send import *
from client import *

def MailClassify(name):
    return ft.TextField(value="dang chon "+name)

def HomePage(page: ft.Page):
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

    

    page.add(mailClass,curMail,sentMail,trashCan, composeMail)
   
   

if __name__ == "__main__":
    ft.app(target=HomePage)

     
     

    
