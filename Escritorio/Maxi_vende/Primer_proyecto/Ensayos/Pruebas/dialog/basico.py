from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class DialogApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return MDScreen(
            MDRaisedButton(
                text="Mostrar Diálogo",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                on_release=self.show_dialog
            )
        )

    def show_dialog(self, obj):
        if not hasattr(self, 'dialog'):
            self.dialog = MDDialog(
                title="Título del Diálogo",
                text="Este es un diálogo simple usando KivyMD.",
                buttons=[
                    MDRaisedButton(
                        text="CERRAR",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()


if __name__ == "__main__":
    DialogApp().run()