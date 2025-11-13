# update/apk_downloader.py
import requests
from kivy.clock import Clock

def descargar_apk(url, ruta_destino, progreso_callback=None, completado_callback=None):
    try:
        with requests.get(url, stream=True) as r:
            total = int(r.headers.get('content-length', 0))
            descargado = 0

            with open(ruta_destino, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        descargado += len(chunk)
                        if progreso_callback:
                            progreso = int((descargado / total) * 100)
                            Clock.schedule_once(lambda dt: progreso_callback(progreso), 0)
        if completado_callback:
            Clock.schedule_once(lambda dt: completado_callback(), 0)
    except Exception as e:
        print("Error al descargar el APK:", e)
