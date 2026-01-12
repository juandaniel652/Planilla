def abrir_archivo (ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return f.read()