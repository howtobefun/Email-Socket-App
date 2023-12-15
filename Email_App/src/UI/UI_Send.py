import flet as ft
from UI_User import *
import Pop_Available

class FileContainerComponent:
    def __init__(self, file_path: str, file_name: str, delete_file: callable):
        self.file_path = file_path
        self.file_name = file_name
        self.delete_file = delete_file

    def remove_file_from_list(self, e):
        self.delete_file(self)

class PickFileSystem(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.add_file)
        self.file_bar = ft.Row(scroll=True)
        self.file_path = []

    def build(self):
        self.page.overlay.append(self.file_picker)
        return ft.Column(
            controls=[
                ft.ElevatedButton("Choose files",
                                  on_click=lambda _: self.file_picker.pick_files(allow_multiple=True)),
                self.file_bar,
            ]
        )

    def find_control_by_path(self, path: str):
        for control in self.file_bar.controls:
            if control.key == path:
                return control
        return None

    def delete_file(self, file_container_component: FileContainerComponent):
        control_to_delete = self.find_control_by_path(file_container_component.file_path)
        if control_to_delete is None:
            return
        self.file_path.remove(file_container_component.file_path)
        self.file_bar.controls.remove(control_to_delete)
        del file_container_component
        self.update()

    def add_file(self, e: ft.FilePickerResultEvent):
        if e.files is None:
            return
        file_over_size_path = ""
        for x in e.files:
            if x.size < 3000000:
                file_container_component = FileContainerComponent(x.path, x.name, self.delete_file)
                file_picked = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(value=x.name),
                            ft.IconButton(
                                ft.icons.DELETE,
                                on_click=file_container_component.remove_file_from_list
                            )
                        ]
                    ),
                    bgcolor=ft.colors.BLUE_100,
                    key=x.path
                )
                self.file_bar.controls.append(file_picked)
                self.file_path.append(x.path)
            else:
                if file_over_size_path == "":
                    file_over_size_path = x.name
                else:
                    file_over_size_path = file_over_size_path + "\n" + x.name

        self.update()
        if file_over_size_path != "":
            file_over_size_alert_dialog = ft.AlertDialog(title=ft.Text("Can't send file > 3MB"),
                                                          content=ft.Text(file_over_size_path))
            self.page.dialog = file_over_size_alert_dialog
            file_over_size_alert_dialog.open = True
            self.page.update()

class SendPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.user = User()
        self.page = page

        self.to = ft.TextField(label="To", height=40)
        self.cc = ft.TextField(label="Cc", height=40)
        self.bcc = ft.TextField(label="Bcc", height=40)
        self.subject = ft.TextField(label="Subject", height=40)
        self.content = ft.TextField(label="Content", min_lines=8, multiline=True, height=220)
        self.send_button = ft.ElevatedButton(text="Send", on_click=self.send)
        self.sent_announce = ft.SnackBar(ft.Text("Sent Successfully"))
        self.file = PickFileSystem(self.page)
        self.sending_progress_bar=ft.Container(
            content=ft.Column([
                ft.Text("Sending...", style="headlineSmall",color=ft.colors.BLUE_900),
                ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee")
            ]),
            alignment=ft.alignment.center,
            width=780,
            height=80,
            bgcolor=ft.colors.BLACK26
        )

    def send(self, e):
        if self.to.value:
            Pop_Available.pop_available=False
            self.page.overlay.append(self.sending_progress_bar)
            self.page.update()
            self.user.smtp_client.send_email(
                mail_to_str=self.to.value,
                cc_str=self.cc.value,
                bcc_str=self.bcc.value,
                subject=self.subject.value,
                content=self.content.value,
                attachments=", ".join(self.file.file_path)
            )
            self.page.overlay.remove(self.sending_progress_bar)
            self.sent_announcement()
            Pop_Available.pop_available=True
            self.page.update()

    def build(self):
        return ft.Column(
            controls=[
                self.to, self.cc, self.bcc,
                self.subject,
                self.file,
                self.content,
                ft.Row([self.send_button], alignment=ft.MainAxisAlignment.END),
            ],
            alignment=ft.MainAxisAlignment.START
        )
    
    def sent_announcement(self):
        self.page.snack_bar = self.sent_announce
        self.sent_announce.open = True
        self.page.update()
