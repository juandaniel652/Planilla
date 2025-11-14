import json
import os


TEMP_FILE = "productos_temp.json"


def guardar_productos_temp(lista_productos_dict):
    try:
        with open(TEMP_FILE, "w", encoding="utf-8") as f:
            json.dump(lista_productos_dict, f, indent=4)
    except Exception as e:
        print(f"[Persistencia] Error al guardar: {e}")

def cargar_productos_temp():
    if not os.path.exists(TEMP_FILE):
        return []
    try:
        with open(TEMP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Persistencia] Error al cargar: {e}")
        return []

def eliminar_productos_temp():
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)