from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from functools import partial


class MyApp(MDApp):
    def build(self):
        self.screen = MDScreen()
        self.datos = {
            "2025-05-01": [("Juan", 10), ("Ana", 20)],
            "2025-05-02": [("Luis", 15), ("Maria", 25)]
        }

        # Lista principal de fechas
        for fecha in self.datos.keys():
            item = OneLineListItem(text=f"Ver recaudación: {fecha}")
            item.bind(on_release=partial(self.mostrar_dialogo_columnas, fecha))
            self.screen.add_widget(item)

        # Crear GridLayout reutilizable para el contenido del diálogo
        self.grid = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.grid)

        self.dialog = MDDialog(
            title="Recaudación",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDRaisedButton(text="Cerrar", on_release=lambda x: self.dialog.dismiss())
            ],
            size_hint_y=0.5,
        )

        return self.screen

    def mostrar_dialogo_columnas(self, instance, fecha):
        # Limpiar la grilla
        self.grid.clear_widgets()

        # Agregar encabezados si deseas
        self.grid.add_widget(MDLabel(text="[b]Nombre[/b]", markup=True))
        self.grid.add_widget(MDLabel(text="[b]Monto[/b]", markup=True))

        for nombre, monto in self.datos.get(fecha, []):
            self.grid.add_widget(MDLabel(text=nombre))
            self.grid.add_widget(MDLabel(text=f"${monto}"))

        self.dialog.title = f"Recaudación del {fecha}"
        self.dialog.open()

MyApp().run()