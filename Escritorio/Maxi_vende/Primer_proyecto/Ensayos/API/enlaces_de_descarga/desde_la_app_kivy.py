import requests
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

try : 
    ANDROID = True
    from jnius import autoclass, cast   #type: ignore
    from android import activity, mActivity #type: ignore
    from android.storage import primary_external_storage_path   #type: ignore
    from android.os import Environment  #type: ignore
    
except ImportError: 
    # Si no se puede importar jnius, significa que no estamos en Android
    ANDROID = False

VERSION_LOCAL = "1.0.0"
VERSION_URL = "https://drive.google.com/uc?export=download&id=1nrFf1XRw6NfWUgX40YLSIsEI11BWURm7"
APK_URL = "https://drive.google.com/uc?export=download&id=1Sd_tj-U9t2VB6f1gL4emjb0SKP_CYuoD"


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
    label = Label(text="¡Hay una nueva versión disponible!\n¿Desea actualizar?")
    btn = Button(text="Descargar ahora", size_hint=(1, 0.3))
    layout.add_widget(label)
    layout.add_widget(btn)
    popup = Popup(title="Actualización", content=layout, size_hint=(0.8, 0.4))

    def descargar_apk(*args):
        popup.dismiss()
        mostrar_popup_descarga()
        descargar_y_guardar_apk()

    btn.bind(on_release=descargar_apk)
    popup.open()

def mostrar_popup_descarga():
    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    label = Label(text="Descargando actualización...")
    progress_bar = ProgressBar(max=100)
    layout.add_widget(label)
    layout.add_widget(progress_bar)
    popup = Popup(title="Descargando", content=layout, size_hint=(0.8, 0.3), auto_dismiss=False)

    # Guardar referencias para actualizar luego
    mostrar_popup_descarga.popup = popup
    mostrar_popup_descarga.label = label
    mostrar_popup_descarga.progress_bar = progress_bar

    popup.open()

def descargar_y_guardar_apk():
    try:
        respuesta = requests.get(APK_URL, stream=True)
        if respuesta.status_code == 200:
            total = int(respuesta.headers.get('content-length', 0))
            nombre_archivo = "nueva_version.apk"
            ruta = os.path.join(os.path.expanduser("~"), "Download", nombre_archivo)

            with open(ruta, "wb") as f:
                descargado = 0
                for chunk in respuesta.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        descargado += len(chunk)
                        porcentaje = int((descargado / total) * 100)
                        Clock.schedule_once(lambda dt, p=porcentaje: actualizar_progreso(p), 0)

            mostrar_popup_descarga.popup.dismiss()
            mostrar_popup_exito(ruta)
        else:
            mostrar_popup_error("Error al descargar el APK.")
    except Exception as e:
        mostrar_popup_error(f"Descarga fallida: {e}")

def actualizar_progreso(porcentaje):
    bar = mostrar_popup_descarga.progress_bar
    label = mostrar_popup_descarga.label
    bar.value = porcentaje
    label.text = f"Descargando... {porcentaje}%"


def abrir_archivo_apk(ruta):
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
        mostrar_popup_error(f"No se pudo abrir el instalador:\n{e}")


def mostrar_popup_exito(ruta):
    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    label = Label(text=f"¡Descarga completa!\nAPK guardado en:\n{ruta}")
    btn = Button(text="OK", size_hint=(1, 0.3))
    layout.add_widget(label)
    layout.add_widget(btn)
    popup = Popup(title="Éxito", content=layout, size_hint=(0.8, 0.4))
    btn.bind(on_release=popup.dismiss)
    popup.open()

def mostrar_popup_error(mensaje):
    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    label = Label(text=mensaje)
    btn = Button(text="Cerrar", size_hint=(1, 0.3))
    layout.add_widget(label)
    layout.add_widget(btn)
    popup = Popup(title="Error", content=layout, size_hint=(0.8, 0.4))
    btn.bind(on_release=popup.dismiss)
    popup.open()