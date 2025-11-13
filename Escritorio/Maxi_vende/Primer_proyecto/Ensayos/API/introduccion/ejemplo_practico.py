import requests
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

VERSION_LOCAL = "1.0.0"
VERSION_URL = "https://tu-servidor.com/version.txt"
APK_URL = "https://tu-servidor.com/miapp.apk"

def verificar_actualizacion():
    try:
        respuesta = requests.get(VERSION_URL)
        if respuesta.status_code == 200:
            version_remota = respuesta.text.strip()
            if version_remota != VERSION_LOCAL:
                mostrar_popup_actualizacion()
    except Exception as e:
        print("Error al verificar versión:", e)

def mostrar_popup_actualizacion():
    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    label = Label(text="¡Hay una nueva versión de la aplicación!\n¿Desea actualizar?")
    btn = Button(text="Actualizar ahora", size_hint=(1, 0.3))
    layout.add_widget(label)
    layout.add_widget(btn)
    popup = Popup(title="Actualización disponible", content=layout, size_hint=(0.8, 0.4))
    
    def abrir_descarga(*args):
        import webbrowser
        webbrowser.open(APK_URL)
        popup.dismiss()
    
    btn.bind(on_release=abrir_descarga)
    popup.open()
