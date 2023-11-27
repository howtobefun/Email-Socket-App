import flet as ft
from UI_Home import *

def initUser(username: str, email: str, password: str):
    configData = initConfigData()
    SMTPclient = Client_SMTP(
        mailserver= configData.Mailserver.ServerIP,
        port = configData.Mailserver.SMTPport,
        username= username,
        password= password,
        email= email
    )
    POP3client = Client_POP3(
        mailserver= configData.Mailserver.ServerIP,
        port = configData.Mailserver.POP3port,
        username= username,
        password= password
    )

    user = User(SMTPclient= SMTPclient, POP3client= POP3client)
    return user

def LoginPage(page:ft.page):
    page.title = "Email Client"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width=800
    page.window_height=700
    #page.window_resizable=False

    userName= ft.TextField(label="User's Name")
    userEmail= ft.TextField(label="User's Email")
    userPassword= ft.TextField(label="User's Password",password=True)
    
    def login(e):#e để nhận tín hiệu từ nút
        if all([userName.value,userEmail.value,userPassword.value]):
            user = initUser(userName.value, userEmail.value, userPassword.value)
            page.controls.pop()
            page.clean()
            HomePage(page)

    loginButton=ft.ElevatedButton(text="Login",on_click=login)
    
    page.add(
            ft.Column(
                [
                    userName,userEmail,userPassword
                ],
                alignment=ft.MainAxisAlignment.START
                ),
            ft.Row([loginButton],alignment=ft.MainAxisAlignment.END)
        )


if __name__ == "__main__":
    ft.app(target=LoginPage)