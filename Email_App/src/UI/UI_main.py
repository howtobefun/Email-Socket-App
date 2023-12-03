from UI_Login import *

def MainPage(page:ft.page):
    page.add(LoginPage(page))


if __name__ == "__main__":
    ft.app(target=MainPage)