# app_main.py - Plantilla para manejo de descarga e instalación de APK con soporte para Android

import os
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

VERSION_LOCAL = "1.0.0"
VERSION_URL = "https://drive.google.com/uc?export=download&id=1nrFf1XRw6NfWUgX40YLSIsEI11BWURm7"
APK_URL = "https://drive.google.com/uc?export=download&id=1Sd_tj-U9t2VB6f1gL4emjb0SKP_CYuoD"

# Detectar si estamos en Android
try:
    from jnius import autoclass, cast #type: ignore
    from android import mActivity #type: ignore
    ANDROID = True
except ImportError:
    ANDROID = False

class Actualizador(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        self.label = Label(text="Verificando versión...")
        self.add_widget(self.label)
        Clock.schedule_once(lambda dt: self.verificar_actualizacion(), 1)

    def verificar_actualizacion(self):
        try:
            r = requests.get(VERSION_URL)
            if r.status_code == 200 and r.text.strip() != VERSION_LOCAL:
                self.mostrar_popup_actualizacion()
            else:
                self.label.text = "La app está actualizada."
        except Exception as e:
            self.label.text = f"Error al verificar versión: {e}"

    def mostrar_popup_actualizacion(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text="¡Hay una nueva versión! ¿Desea actualizar?")
        btn = Button(text="Descargar", size_hint=(1, 0.3))
        layout.add_widget(label)
        layout.add_widget(btn)
        popup = Popup(title="Actualización", content=layout, size_hint=(0.8, 0.4))

        def descargar_apk(_):
            popup.dismiss()
            self.popup_descarga = self.mostrar_popup_descarga()
            self.descargar_y_guardar_apk()

        btn.bind(on_release=descargar_apk)
        popup.open()

    def mostrar_popup_descarga(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(text="Descargando...")
        barra = ProgressBar(max=100)
        layout.add_widget(label)
        layout.add_widget(barra)
        popup = Popup(title="Descargando", content=layout, size_hint=(0.8, 0.3), auto_dismiss=False)
        popup.open()
        self.popup_barra = barra
        self.popup_label = label
        return popup

    def descargar_y_guardar_apk(self):
        try:
            r = requests.get(APK_URL, stream=True)
            if r.status_code == 200:
                total = int(r.headers.get('content-length', 0))
                nombre = "nueva_version.apk"
                ruta = os.path.join(os.path.expanduser("~"), "Download", nombre)
                with open(ruta, "wb") as f:
                    descargado = 0
                    for chunk in r.iter_content(1024):
                        if chunk:
                            f.write(chunk)
                            descargado += len(chunk)
                            porcentaje = int((descargado / total) * 100)
                            Clock.schedule_once(lambda dt, p=porcentaje: self.actualizar_progreso(p), 0)
                self.popup_descarga.dismiss()
                self.abrir_archivo_apk(ruta)
            else:
                self.popup_label.text = "Error al descargar."
        except Exception as e:
            self.popup_label.text = f"Fallo descarga: {e}"

    def actualizar_progreso(self, porcentaje):
        self.popup_barra.value = porcentaje
        self.popup_label.text = f"Descargando... {porcentaje}%"

    def abrir_archivo_apk(self, ruta):
        if not ANDROID:
            self.popup_label.text = f"APK descargado en: {ruta}"
            return
        
        try:
            File = autoclass('java.io.File')
            Uri = autoclass('android.net.Uri')
            Intent = autoclass('android.content.Intent')
            FileProvider = autoclass('androidx.core.content.FileProvider')
            context = mActivity.getApplicationContext()
            file = File(ruta)
            uri = FileProvider.getUriForFile(context, context.getPackageName() + ".provider", file)

            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, "application/vnd.android.package-archive")
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            mActivity.startActivity(intent)

        except Exception as e:
            self.popup_label.text = f"Error al abrir instalador: {e}"

class MiApp(App):
    def build(self):
        return Actualizador()

if __name__ == '__main__':
    MiApp().run()
