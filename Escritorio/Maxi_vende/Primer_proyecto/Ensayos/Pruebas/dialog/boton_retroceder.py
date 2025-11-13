from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp

class MyApp(MDApp):
    def build(self):
        self.dialog = MDDialog(
            title="",
            type="custom",
            size_hint_y=0.6
        )

        return MDRaisedButton(text="Abrir Historial", on_release=lambda x: self.mostrar_historial())

    def mostrar_historial(self, *args):
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(MDLabel(text="Esta es la SECCIÓN 1 (Historial)"))
        layout.add_widget(MDRaisedButton(text="Ir a Recaudación", on_release=lambda x: self.mostrar_recaudacion("2025-05-01")))

        self.dialog.title = "Historial"
        self.dialog.content_cls = layout
        self.dialog.buttons = [
            MDRaisedButton(text="Cerrar", on_release=lambda x: self.dialog.dismiss())
        ]

        if not self.dialog._window:
            self.dialog.open()

    def mostrar_recaudacion(self, titulo, *args):
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(MDLabel(text=f"Recaudación del {titulo}"))

        self.dialog.title = f"Recaudación de {titulo}"
        self.dialog.content_cls = layout
        self.dialog.buttons = [
            MDRaisedButton(text="Atrás", on_release=self.mostrar_historial),
            MDRaisedButton(text="Cerrar", on_release=lambda x: self.dialog.dismiss())
        ]

# Ejecutar
MyApp().run()

