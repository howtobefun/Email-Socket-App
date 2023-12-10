from UI_Login import *
from UI_Home import *
from UI_Send import *
from UI_Receive import *
from urllib.parse import urlparse

def main_page(page: ft.Page):
    def setup_page():
        page.title = "Email Client"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.window_width = 800
        page.window_height = 700
        page.scroll = True

    # To change the page, use page.go()
    # To add obj to the page, use page.views[-1].controls.append()

    def route_change(e):  # Function is called whenever the route changes (page.go())
        if page.route == '/':  # Default '/' so not changed to '/Login'
            if page.views:
                if page.views[-1].route == '/':
                    page.update()
                    return
            page.views.append(
                ft.View(
                    route='/',
                    controls=[
                        ft.AppBar(title=ft.Text('Login'), bgcolor=ft.colors.BLUE_50),
                        LoginPage(page)
                    ]
                )
            )

        if page.route == '/Home' and page.views[-1].route != '/Home':
            page.views.append(
                ft.View(
                    route='/Home',
                    controls=[
                        ft.AppBar(title=ft.Text('Home'), bgcolor=ft.colors.BLUE_50),
                        HomePage(page)
                    ]
                )
            )

        if page.route == '/Compose' and page.views[-1].route != '/Compose':
            page.views.append(
                ft.View(
                    route='/Compose',
                    controls=[
                        ft.AppBar(title=ft.Text('Compose'), bgcolor=ft.colors.BLUE_50),
                        SendPage(page)
                    ]
                )
            )

        param = page.route
        res = urlparse(param).path.split(", ")[-1]
        if page.route == f"/Receive, {res}" and page.views[-1].route != f"/Receive, {res}":
            page.views.append(
                ft.View(
                    route=f"/Receive, {res}",
                    controls=[
                        ft.AppBar(title=ft.Text('Receive'), bgcolor=ft.colors.BLUE_50),
                        ReceivePage(page, res)
                    ]
                )
            )

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    setup_page()
    page.views.clear()
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main_page)
