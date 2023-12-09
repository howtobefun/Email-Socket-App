from UI_Login import *
from UI_Home import *
from UI_Send import *
from UI_Receive import *
from urllib.parse import urlparse

def MainPage(page:ft.page):
    # def openDialog(e):
    #     fileOverSize=ft.AlertDialog(title=ft.Text("Can't send file > 1MB"),content=ft.Text(""))
    #     page.dialog = fileOverSize
    #     fileOverSize.open=True
    #     page.update()

    # page.add(ft.Row([ft.TextButton(text="open dialog",on_click=openDialog)]))


    def setupPage():
        page.title = "Email Client"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.window_width=800
        page.window_height=700
        page.scroll=True

    #muốn chuyển page thì page.go()
    #muốn page.add thì page.views[-1].controls.append()

    def route_change(e): #function is called when ever the route changed (page.go())
        if page.route=='/': #default '/' nên tui ko đổi thành '/Login'
            if page.views: 
                if page.views[-1].route=='/':
                    page.update()
                    return
            page.views.append(
                ft.View(
                    route='/',
                    controls=[
                        ft.AppBar(title=ft.Text('Login'),bgcolor=ft.colors.BLUE_50),
                        LoginPage(page)
                    ]
                )
            )

        if page.route=='/Home' and page.views[-1].route!='/Home':
            page.views.append(
                ft.View(
                    route='/Home',
                    controls=[
                        ft.AppBar(title=ft.Text('Home'),bgcolor=ft.colors.BLUE_50),
                        HomePage(page)
                    ]
                )
            )

        if page.route=='/Compose' and page.views[-1].route!='/Compose':
            page.views.append(
                ft.View(
                    route='/Compose',
                    controls=[
                        ft.AppBar(title=ft.Text('Compose'),bgcolor=ft.colors.BLUE_50),
                        SendPage(page)
                    ]
                )
            )
        
        param=page.route
        res=urlparse(param).path.split(", ")[-1]
        if page.route==f"/Receive, {res}" and page.views[-1].route!=f"/Receive, {res}":
            page.views.append(
                ft.View(
                    route=f"/Receive, {res}",
                    controls=[
                        ft.AppBar(title=ft.Text('Receive'),bgcolor=ft.colors.BLUE_50),
                        ReceivePage(page,res)
                    ]
                )
            )

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    setupPage()
    page.views.clear()
    page.on_route_change=route_change
    page.on_view_pop=view_pop
    page.go(page.route)
    


if __name__ == "__main__":
    ft.app(target=MainPage)