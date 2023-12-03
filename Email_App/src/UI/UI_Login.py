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


class LoginPage(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page=page
        self.setupPage()

        self.userName= ft.TextField(label="User's Name")
        self.userEmail= ft.TextField(label="User's Email")
        self.userPassword= ft.TextField(label="User's Password",password=True)

        self.loginButton=ft.ElevatedButton(text="Login",on_click=self.login)
         
    def setupPage(self):
        self.page.title = "Email Client"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.window_width=800
        self.page.window_height=700
        self.page.scroll=True

    def login(self,e):
        if all([self.userName.value,self.userEmail.value,self.userPassword.value]):
            self.user = initUser(self.userName.value, self.userEmail.value, self.userPassword.value)
            self.page.controls.pop()
            self.page.clean()
            self.page.add(HomePage(self.page))
       
    def build(self):
        return ft.Column(
                controls=[
                    self.userName,self.userEmail,self.userPassword,
                    ft.Row([self.loginButton],alignment=ft.MainAxisAlignment.END)
                ],
                alignment=ft.MainAxisAlignment.START
            )
            


def LoginMain(page:ft.page):
    page.add(LoginPage(page))


if __name__ == "__main__":
    ft.app(target=LoginMain)