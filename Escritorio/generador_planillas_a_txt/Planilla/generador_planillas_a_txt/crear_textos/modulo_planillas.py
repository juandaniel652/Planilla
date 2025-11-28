import os
import re
from datetime import datetime

# ============================
#   TUS FUNCIONES ORIGINALES
# ============================

def limpiar_nombre(nombre):
    nombre = nombre.strip().rstrip('.')
    if nombre.count('(') > nombre.count(')'):
        nombre += ')'
    return nombre

def extraer_fecha(linea):
    match = re.search(r'(\d{2}/\d{2}/\d{2})', linea)
    if match:
        fecha = match.group(1)
        fecha = re.sub(r'[^\d/]', '', fecha)
        return fecha, match.start()
    return None, None

def normalizar_y_ordenar_planilla_robusto(texto):
    lineas = [l.strip() for l in texto.strip().splitlines() if l.strip()]
    personas = []
    fechas = []

    for linea in lineas:
        fecha, idx = extraer_fecha(linea)
        if fecha:
            fechas.append(fecha)
            nombre = linea[:idx].strip()
            if nombre:
                personas.append(nombre)
        else:
            personas.append(linea)

    asignaciones = []
    idx_fecha = 0

    for persona in personas:
        persona = limpiar_nombre(persona)
        tiene_letra = re.search(r'\([a-zA-Z,\s\-]+\)', persona)
        persona_final = persona if tiene_letra else f"{persona} (Completo)"

        fecha_inicio = fechas[idx_fecha] if idx_fecha < len(fechas) else None
        fecha_fin = fechas[idx_fecha+1] if idx_fecha+1 < len(fechas) else None

        if fecha_inicio:
            try:
                fecha_inicio_obj = datetime.strptime(fecha_inicio, "%d/%m/%y")
            except ValueError:
                fecha_clean = re.sub(r'[^\d/]', '', fecha_inicio)
                fecha_inicio_obj = datetime.strptime(fecha_clean, "%d/%m/%y")
        else:
            fecha_inicio_obj = datetime.max

        if fecha_inicio and fecha_fin:
            asignaciones.append((fecha_inicio_obj, f'"{persona_final} {fecha_inicio}   {fecha_fin}"'))
            idx_fecha += 2
        elif fecha_inicio:
            asignaciones.append((fecha_inicio_obj, f'"{persona_final} {fecha_inicio}"'))
            idx_fecha += 1
        else:
            asignaciones.append((fecha_inicio_obj, f'"{persona_final}"'))

    asignaciones.sort(key=lambda x: x[0])
    return [a[1] for a in asignaciones]

def procesar_territorios(texto):
    lineas = [l.strip() for l in texto.strip().splitlines() if l.strip()]
    bloques = {}
    territorio_actual = None
    buffer = []

    for linea in lineas:
        if re.fullmatch(r'\d+', linea):
            if territorio_actual is not None:
                bloques[territorio_actual] = buffer
            territorio_actual = linea
            buffer = []
        else:
            buffer.append(linea)

    if territorio_actual is not None:
        bloques[territorio_actual] = buffer

    resultado_final = []
    for territorio, bloque in sorted(bloques.items(), key=lambda x: int(x[0])):
        resultado_final.append(f"\n\n================ Territorio {territorio} ================\n")
        bloque_texto = "\n".join(bloque)
        asignaciones = normalizar_y_ordenar_planilla_robusto(bloque_texto)
        resultado_final.extend(asignaciones)

    return resultado_final

# =================================================================
#   NUEVO: crear carpeta + exportar resultados en archivos .txt
# =================================================================

def generar_txt_planilla(nombre_planilla, texto):
    """
    Procesa la planilla y genera un archivo .txt en la carpeta:
        datos_en_formato_texto/
    """

    # --- 1. Crear carpeta si no existe ---
    carpeta = "datos_en_formato_texto"
    os.makedirs(carpeta, exist_ok=True)

    # --- 2. Limpiar el nombre para usar como archivo ---
    nombre_archivo = nombre_planilla.replace("/", "-").replace("\\", "-")
    ruta = os.path.join(carpeta, f"{nombre_archivo}.txt")

    # --- 3. Procesar ---
    resultado = procesar_territorios(texto)

    # --- 4. Guardar en TXT ---
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(nombre_planilla + "\n\n")
        for linea in resultado:
            f.write(linea + "\n")

    return ruta   # devuelve ruta del archivo creado
