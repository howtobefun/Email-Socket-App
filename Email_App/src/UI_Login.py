import flet as ft
from UI_Home import*

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
    username = sender
    password = "password"

    SMTPclient = Client_SMTP(mailserver, SMTPport, username)
    ft.app(target=LoginPage)