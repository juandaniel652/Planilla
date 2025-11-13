#POCO EFICIENTE, CREA MÁS Y NO ELIMINA LOS ANTERIORES, POR ENDE EN EL ARCHIVO LLAMADO
#SEGUNDO_DIALOG_EN_UNO.PY APARECE CON ESAS FUNCIONALIDAD

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

        # Datos de prueba (fecha, total)
        datos = [
            ("2025-05-01", 100),
            ("2025-05-02", 150)
        ]

        for item in datos:
            texto = f"Fecha = {item[0]} || Total recaudado = {item[1]}"
            fila = OneLineListItem(text=texto)
            fila.bind(on_release=partial(self.mostrar_dialogo, fecha=item[0]))
            self.lista_principal.add_widget(fila)

        return self.screen

    def mostrar_dialogo(self, instance, fecha):
        print(f"Abriendo diálogo para la fecha: {fecha}")

        # Crear lista secundaria con datos simulados según la fecha
        datos_secundarios = {
            "2025-05-01": [("Juan", 10), ("Ana", 20)],
            "2025-05-02": [("Luis", 15), ("Maria", 25)]
        }

        lista_datos = datos_secundarios.get(fecha, [])

        # Crear ScrollView + MDList para el diálogo
        scroll = ScrollView()
        lista_dialogo = MDList()
        scroll.add_widget(lista_dialogo)

        for nombre, monto in lista_datos:
            texto = f"{nombre} — ${monto}"
            lista_dialogo.add_widget(OneLineListItem(text=texto))

        # Crear y mostrar el MDDialog con contenido personalizado
        self.dialog = MDDialog(
            title=f"Recaudación del {fecha}",
            type="custom",
            content_cls=scroll,
            size_hint_y=0.5,
        )
        self.dialog.open()


MyApp().run()
