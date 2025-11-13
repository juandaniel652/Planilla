from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

def mostrar_popup():
    layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
    layout.add_widget(Label(text='Este es un popup', color=(1, 1, 1, 1)))

    btn_cerrar = Button(text='Cerrar', background_color=(0, 0.6, 0, 1), color=(1, 1, 1, 1))
    btn_cerrar.bind(on_release=lambda x: popup.dismiss())
    layout.add_widget(btn_cerrar)

    popup = Popup(title='Información',
                  content=layout,
                  size_hint=(None, None), size=(400, 200),
                  background_color=(0.1, 0.1, 0.1, 0.95),
                  title_color=(1, 1, 1, 1))
    popup.open()

mostrar_popup()