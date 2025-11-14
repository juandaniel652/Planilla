from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

def crear_caja_emergente (titulo, texto) : 

        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        message = Label(
        text = texto,
        font_name = "Roboto_Mono_contenido",
        font_size = '15sp',
        color = '#FFFFFF',
        halign = 'center',
        valign = 'middle'
        )

        message.bind(size=message.setter('text_size'))

        boton_cerrar = Button(
            text = "Cerrar",
            font_name = "Ancizar_botones",
            size_hint_y = None,
            height = 30,
            background_color = '#00C853',
            color = '#FFFFFF',  
            bold = True
        )

        content.add_widget(message)
        content.add_widget(boton_cerrar)

        popup = Popup(
            title = titulo, 
            title_size = 20, 
            title_align = 'center',
            title_color = (1, 1, 1, 1),
            title_font = "Roboto_Mono_titulo",
            background_color = '#1f1f1f',
            separator_color = '#00C853',
            size_hint=(0.8, 0.4),
            content = content,
            auto_dismiss = False,
        )

        boton_cerrar.bind(on_release=popup.dismiss)
        popup.open()
