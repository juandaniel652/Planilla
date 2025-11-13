# actualizador/actualizador.py
import requests
from kivy.clock import Clock
import os

# Ajusta esta constante con la URL directa del .txt en Google Drive
VERSION_ACTUAL = "1.0.0"
VERSION_URL = "https://drive.google.com/uc?export=download&id=1nrFf1XRw6NfWUgX40YLSIsEI11BWURm7"
APK_URL = "https://drive.google.com/uc?export=download&id=1Sd_tj-U9t2VB6f1gL4emjb0SKP_CYuoD"

APK_PATH = "komproventa-1.0.0-arm64-v8a_armeabi-v7a-release-unsigned.apk"  # O ruta alternativa válida en Android

class Actualizador:
    def __init__(self, version_actual=VERSION_ACTUAL, url_txt=VERSION_URL):
        self.version_actual = version_actual
        self.url_txt = url_txt
        self.info_actualizacion = None

    def verificar_actualizacion(self):
        try:
            r = requests.get(self.url_txt, timeout=5)
            if r.status_code == 200:
                contenido = r.text.strip()
                version_nueva, apk_url = contenido.split('|')
                if version_nueva.strip() != self.version_actual:
                    self.info_actualizacion = {
                        "version": version_nueva.strip(),
                        "apk_url": apk_url.strip()
                    }
                    return self.info_actualizacion
        except Exception as e:
            print(f"[Actualizador] Error verificando actualización: {e}")
        return None

    def descargar_apk(self, progreso_callback=None, completado_callback=None):
        if not self.info_actualizacion:
            return

        try:
            url = self.info_actualizacion["apk_url"]
            r = requests.get(url, stream=True)
            total = int(r.headers.get('content-length', 0))
            descargado = 0

            with open(APK_PATH, 'wb') as f:
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        descargado += len(chunk)
                        if progreso_callback:
                            progreso = int((descargado / total) * 100)
                            Clock.schedule_once(lambda dt: progreso_callback(progreso), 0)

            if completado_callback:
                Clock.schedule_once(lambda dt: completado_callback(), 0)

        except Exception as e:
            print(f"[Actualizador] Error descargando el APK: {e}")

    def instalar_apk(self):
        try:
            from jnius import autoclass #type: ignore
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')

            context = PythonActivity.mActivity
            file = File(APK_PATH)
            uri = Uri.fromFile(file)
            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, "application/vnd.android.package-archive")
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(intent)

        except Exception as e:
            print(f"[Actualizador] Error al intentar instalar el APK: {e}")
