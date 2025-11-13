# main.py (fragmento)
from update.version_checker import get_latest_version_info_txt

API_TXT_URL = "https://drive.google.com/uc?export=download&id=1nrFf1XRw6NfWUgX40YLSIsEI11BWURm7"

# Dentro de tu clase MainScreen
def verificar(self):
    self.info = get_latest_version_info_txt(API_TXT_URL)
    if self.info:
        if self.info["version"] != "1.0.0":  # Reemplaza con la versión actual de la app
            self.label.text = f"Nueva versión {self.info['version']} disponible"
            self.boton.disabled = False
        else:
            self.label.text = "La app está actualizada"
    else:
        self.label.text = "No se pudo verificar la actualización"
