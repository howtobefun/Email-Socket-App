import flet as ft

def TestPage(page:ft.page):
        
    #def login(e):#e để nhận tín hiệu từ nút
        # if all([userName.value,userEmail.value,userPassword.value]):
        #     user = initUser(userName.value, userEmail.value, userPassword.value)
        #     page.controls.pop()
        #     page.clean()
    
    show=ft.Container(
        content=ft.Column([
            ft.Container( ft.TextField(value="aaa",border=False,width=100)),
            ft.Container(ft.IconButton(ft.icons.RESTORE_FROM_TRASH_ROUNDED))
            ]   
        )
    )
    show.expand(ft.Column([
            ft.Container( ft.TextField(value="bbb",border=False,width=100)),
            ft.Container(ft.IconButton(ft.icons.RESTORE_FROM_TRASH_ROUNDED))
            ]   
        ))
    show.
    page.add(show)
    #loginButton=ft.ElevatedButton(text="Login",on_click=login)



if __name__ == "__main__":
    ft.app(target=TestPage)

