from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.uix.scrollview import ScrollView
from functools import partial


class MyApp(MDApp):
    def build(self):
        self.screen = MDScreen()
        scroll = ScrollView()
        self.lista_principal = MDList()
        scroll.add_widget(self.lista_principal)
        self.screen.add_widget(scroll)

        # Datos principales
        datos = [
            ("2025-05-01", 100),
            ("2025-05-02", 150)
        ]

        for item in datos:
            texto = f"Fecha = {item[0]} || Total recaudado = {item[1]}"
            fila = OneLineListItem(text=texto)
            fila.bind(on_release=partial(self.mostrar_dialogo, fecha=item[0]))
            self.lista_principal.add_widget(fila)

        # Creamos una vez el MDDialog con ScrollView + MDList vacío
        self.lista_dialogo = MDList()
        scroll_dialogo = ScrollView()
        scroll_dialogo.add_widget(self.lista_dialogo)

        self.dialog = MDDialog(
            title="Recaudación",
            type="custom",
            content_cls=scroll_dialogo,
            size_hint_y=0.5,
        )

        return self.screen

    def mostrar_dialogo(self, instance, fecha):
        print(f"Actualizando diálogo para la fecha: {fecha}")

        # Simulación de datos por fecha
        datos_secundarios = {
            "2025-05-01": [("Juan", 10), ("Ana", 20)],
            "2025-05-02": [("Luis", 15), ("Maria", 25)]
        }

        # Limpiar la lista antes de añadir nuevos widgets
        self.lista_dialogo.clear_widgets()

        for nombre, monto in datos_secundarios.get(fecha, []):
            texto = f"{nombre} — ${monto}"
            self.lista_dialogo.add_widget(OneLineListItem(text=texto))

        # Actualizar el título del diálogo
        self.dialog.title = f"Recaudación del {fecha}"
        self.dialog.open()

MyApp().run()