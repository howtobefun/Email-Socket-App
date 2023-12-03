from UI_Login import *
from UI_Home import *
from UI_Send import *


def MainPage(page:ft.page):
    def setupPage():
        page.title = "Email Client"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.window_width=800
        page.window_height=700
        page.scroll=True
    
    def route_change(e):
        print("route change: ",page.views)
        if page.route=='/':
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