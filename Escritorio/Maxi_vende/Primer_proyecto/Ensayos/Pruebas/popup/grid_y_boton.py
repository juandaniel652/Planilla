from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button

# Crear el layout contenedor
contenedor = BoxLayout(orientation='vertical', spacing=10, padding=10)

# Agregar tu grid (ya creado previamente)
contenedor.add_widget(self.grid) #type: ignore[no-untyped-call]

# Crear y agregar un botón debajo del grid
boton = Button(
    text="Cerrar",
    size_hint=(1, None),
    height=40,
    background_color=(0, 0.7, 0.3, 1),
    color=(1, 1, 1, 1)
)
boton.bind(on_release=lambda *args: popup.dismiss())
contenedor.add_widget(boton)

# Crear el popup con el contenedor como contenido
popup = Popup(
    title=f"Recaudación del {titulo_fecha}", #type: ignore
    title_font="Roboto_Mono_titulo",
    title_size="18sp",
    content=contenedor,
    size_hint=(0.9, 0.7), 
    size=(500, 350),
    background_color='#1f1f1f',
    separator_color='#00C853',
    auto_dismiss=True,
)

popup.open()
