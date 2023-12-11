import flet as ft
from UI_Home import *

def init_user(username: str, email: str, password: str):
    config_data = init_config_data()
    smtp_client = Client_SMTP(
        mailserver=config_data.Mailserver.ServerIP,
        port=config_data.Mailserver.SMTPport,
        username=username,
        password=password,
        email=email
    )
    pop3_client = Client_POP3(
        mailserver=config_data.Mailserver.ServerIP,
        port=config_data.Mailserver.POP3port,
        username=username,
        password=password,
        email=email
    )

    try:
        user = User()
        user.reset(smtp_client=smtp_client, pop3_client=pop3_client)
    except:
        user = User(smtp_client=smtp_client, pop3_client=pop3_client)

    return user

class LoginPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.user_name = ft.TextField(label="User's Name")
        self.user_email = ft.TextField(label="User's Email")
        self.user_password = ft.TextField(label="User's Password", password=True)

        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login)

    def login(self, e):
        if all([self.user_name.value, self.user_email.value, self.user_password.value]):
            self.user = init_user(self.user_name.value, self.user_email.value, self.user_password.value)
            self.page.go('/Home')

    def build(self):
        return ft.Column(
            controls=[
                self.user_name, self.user_email, self.user_password,
                ft.Row([self.login_button], alignment=ft.MainAxisAlignment.END)
            ],
            alignment=ft.MainAxisAlignment.START
        )