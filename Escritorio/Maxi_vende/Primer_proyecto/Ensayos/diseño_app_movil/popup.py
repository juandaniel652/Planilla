from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.scrollview import MDScrollView

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        open_popup_btn = Button(text='Mostrar Grid de 4 columnas', size_hint=(1, 0.2))
        open_popup_btn.bind(on_release=self.show_popup)
        layout.add_widget(open_popup_btn)
        return layout

    def show_popup(self, instance):
        # Crear un GridLayout con 4 columnas
        datos = [('Cafe', 2, 1000.0, 3000.0),
                ('Leche', 1, 2000.0, 2000.0),
                ('Te', 1, 2000.0, 2000.0),
                ('Azucar', 3000.0, 0.5, 1500.0),
                ('Galletas', 5000.0, 0.8, 14000.0)]
        
        grid = GridLayout(cols=4, spacing=10, padding=10)
        
        encabezados = ["Productos", "Cantidad", "Precio", "Total"]
        for subtitulo in encabezados:
            grid.add_widget(Label(text=f"[b]{subtitulo}[/b]", markup=True))

        for item in datos:
            grid.add_widget(Label(text=item[0]))
            grid.add_widget(Label(text=f"{item[1]}"))
            grid.add_widget(Label(text=f"${item[2]}"))
            grid.add_widget(Label(text=f"${item[3]}"))

        # Líneas separadoras y totales
        for _ in range(4):
            grid.add_widget(Label(text="__________"))

        for _ in range(4):
            grid.add_widget(Label(text=""))

        grid.add_widget(Label(text="Total Vendido", bold=True))
        grid.add_widget(Label(text=f"$62000", bold=True))

        for _ in range(2):
            grid.add_widget(Label(text=""))

        grid.add_widget(Label(text="Total Cantidad", bold=True))
        grid.add_widget(Label(text=f"Total", bold=True))


        # Crear y mostrar el Popup
        popup = Popup(
            title='GridLayout de 4 Columnas',
            content=grid,
            size_hint=(0.8, 0.6),  # más ancho para que entren 4 columnas
            auto_dismiss=True
        )
        popup.open()

MainApp().run()
