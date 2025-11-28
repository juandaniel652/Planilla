import re
from datetime import datetime


def convertir_linea(linea: str):
    # limpiar comillas
    linea = linea.strip().strip('"').strip("'")
    if not linea:
        return None

    # normalizar espacios
    linea = re.sub(r"\s+", " ", linea)

    # extraer fechas (formato dd/mm/yy)
    fechas = re.findall(r"\d{2}/\d{2}/\d{2}", linea)
    if len(fechas) != 2:
        return None

    # quitar fechas para analizar nombre y alias
    sin_fechas = re.sub(r"\d{2}/\d{2}/\d{2}", "", linea).strip()

    # extraer nombre antes del primer paréntesis
    partes = sin_fechas.split("(")
    nombre = partes[0].strip()
    if not nombre:
        return None

    # extraer alias sin los paréntesis
    alias_matches = re.findall(r"\((.*?)\)", sin_fechas)
    if not alias_matches:
        alias = "Completo"
    else:
        alias = ", ".join(alias_matches)

    # formatear fechas a YYYY-MM-DD
    def fmt(f):
        return datetime.strptime(f, "%d/%m/%y").strftime("%Y-%m-%d")

    fecha_inicio = fmt(fechas[0])
    fecha_fin = fmt(fechas[1])

    return nombre, fecha_inicio, fecha_fin, alias


def convertir_archivo_completo(texto: str):
    resultados = []
    territorio_actual = None

    for linea in texto.splitlines():
        linea = linea.strip()

        # detectar encabezado de territorio y capturar su número real
        match = re.search(r"Territorio\s+(\d+)", linea, re.IGNORECASE)
        if match:
            territorio_actual = int(match.group(1))
            continue

        # saltar encabezados generales y separadores
        if "planilla" in linea.lower() or linea.startswith("="):
            continue

        tupla = convertir_linea(linea)
        if tupla and territorio_actual is not None:
            nombre, f_asig, f_comp, alias = tupla
            resultados.append((territorio_actual, nombre, f_asig, f_comp, alias))

    return resultados


if __name__ == "__main__":
    texto = open("planilla.txt", encoding="utf-8").read()
    tuplas = convertir_archivo_completo(texto)
    for t in tuplas:
        print(t, ",")
