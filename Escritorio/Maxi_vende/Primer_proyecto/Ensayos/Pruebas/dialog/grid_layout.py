from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

KV = '''
MDScreen:
    MDRaisedButton:
        text: "Mostrar Diálogo"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: app.mostrar_dialogo()

<MyDialog>:
    title: 'Título del cuadro de diálogo'
    md_bg_color: 1, 1, 1, 1
    adaptive_height: True  # Si quieres que se ajuste a la altura del contenido
    size_hint_y: None # Permite que se ajuste a la altura del contenido
    height: self.minimum_height # Establece la altura mínima (opcional)

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        size_hint_y: None

        MDLabel:
            text: 'Este es un ejemplo de cuadro de diálogo con tamaño ajustable.'
            halign: 'center'
            valign: 'middle'
            size_hint_y: None
            height: dp(40)
'''

class DialogConTresColumnas(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "25dp"
        self.padding = [10, 50, 10, 10]  # padding izquierda, ARRIBA, derecha, abajo
        self.size_hint_y = None
        self.height = self.minimum_height

        # Encabezados
        encabezado = MDBoxLayout(orientation='horizontal', spacing="10dp")
        encabezado.add_widget(MDLabel(text="Nombre", bold=True))
        encabezado.add_widget(MDLabel(text="Edad", bold=True))
        encabezado.add_widget(MDLabel(text="Ciudad", bold=True))
        self.add_widget(encabezado)

        # Fila 1
        fila1 = MDBoxLayout(orientation='horizontal', spacing="10dp")
        fila1.add_widget(MDLabel(text="Juan"))
        fila1.add_widget(MDLabel(text="30"))
        fila1.add_widget(MDLabel(text="Madrid"))
        self.add_widget(fila1)

        # Fila 2
        fila2 = MDBoxLayout(orientation='horizontal', spacing="10dp")
        fila2.add_widget(MDLabel(text="Ana"))
        fila2.add_widget(MDLabel(text="25"))
        fila2.add_widget(MDLabel(text="Barcelona"))
        self.add_widget(fila2)


class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def mostrar_dialogo(self):
        contenido = DialogConTresColumnas()
        self.dialogo = MDDialog(
            title="",
            type="custom",
            content_cls=contenido,
            buttons=[
                MDFlatButton(text="CERRAR", on_release=lambda x: self.dialogo.dismiss())
            ]
        )
        self.dialogo.open()

MyApp().run()
