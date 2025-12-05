#Lleva los datos de la planilla ya convertidos a la base de datos MySQL
import mysql.connector
from datetime import datetime
import re
import csv

errores = []

mapa_nombres = {
    r"^f\.?\s*israelson$": "Fernando Israelson",
    r"^a\.?\s*israelson$": "Fernando Israelson",
    r"^juan\s+dominguez$": "Juan Domínguez",
    r"^ju\.?\s*dominguez$": "Juan Domínguez",
    r"^j\.?\s*dom[ií]nguez$": "Joel Domínguez",
    r"^jorge\s+arg[üu]ello$": "Jorge Argüello",
    r"^j\.?\s*arg[üu]ello$": "Jorge Argüello",
    r"^w\.?\s*valiente$": "Walter Valiente",
    r"^walter\s+valiente$": "Walter Valiente",
    r"^l\.?\s*ben[ií]tez$": "Luis Benítez",
    r"^luis\s+ben[ií]tez$": "Luis Benítez",
    r"^n\.?\s*ben[ií]tez$": "Nahuel Benítez",
    r"^nahuel\s+ben[ií]tez$": "Nahuel Benítez",
}

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="miclave123",
    database="Planillas",
    ssl_disabled=True
)

# ✅ Cursor buffered para evitar "Unread result"
cursor = conexion.cursor(buffered=True)

def territorio_existe(numero):
    cursor.execute("SELECT id FROM Territorios WHERE numero = %s", (numero,))
    row = cursor.fetchone()
    return row[0] if row else None

def normalizar_nombre(nombre_original):
    nombre = nombre_original.lower().strip()
    for patron, canonico in mapa_nombres.items():
        if re.match(patron, nombre, flags=re.IGNORECASE):
            return canonico
    return nombre_original.title()

def conductor_existe(nombre):
    cursor.execute("SELECT id FROM Conductores WHERE nombre_completo = %s", (nombre,))
    row = cursor.fetchone()
    return row[0] if row else None

def insertar_territorio(numero):
    cursor.execute("INSERT INTO Territorios (numero) VALUES (%s)", (numero,))
    conexion.commit()
    return territorio_existe(numero)

def insertar_conductor(nombre):
    cursor.execute("INSERT INTO Conductores (nombre_completo) VALUES (%s)", (nombre,))
    conexion.commit()
    return conductor_existe(nombre)

def insertar_asignacion(territorio_id, conductor_id, fecha_asig, fecha_comp, cantidad):
    sql = """INSERT INTO Asignaciones
             (territorio_id, conductor_id, fecha_asignado, fecha_completado, cantidad_abarcado)
             VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(sql, (territorio_id, conductor_id, fecha_asig, fecha_comp, cantidad))
    conexion.commit()

def validar_fechas(fecha_asig, fecha_comp):
    try:
        a = datetime.strptime(fecha_asig, "%Y-%m-%d")
        b = datetime.strptime(fecha_comp, "%Y-%m-%d")
        return b >= a
    except:
        return False

def guardar_errores_csv():
    if errores:
        with open("informe_errores.csv","w",newline="",encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["territorio","nombre","fecha_asig","fecha_comp","motivo"])
            w.writerows(errores)

if __name__ == "__main__":

    tuplas = [
        ]

    for numero, nombre, fecha_asig, fecha_comp, cantidad in tuplas:

        # --- Territorio ---
        terr_id = territorio_existe(numero)
        if terr_id is None:
            print(f"✅ Insertando territorio {numero}")
            terr_id = insertar_territorio(numero)

        # --- Conductor ---
        nombre_unificado = normalizar_nombre(nombre)
        cond_id = conductor_existe(nombre_unificado)
        if cond_id is None:
            print(f"✅ Insertando conductor '{nombre_unificado}'")
            cond_id = insertar_conductor(nombre_unificado)

        # --- Validar fechas ---
        if not validar_fechas(fecha_asig, fecha_comp):
            motivo = "Fecha inválida o fecha_comp < fecha_asig"
            print(f"❌ {motivo} → {numero}, {nombre}, {fecha_asig} → {fecha_comp}")
            errores.append((numero, nombre, fecha_asig, fecha_comp, motivo))
            continue

        # --- Insertar ---
        insertar_asignacion(terr_id, cond_id, fecha_asig, fecha_comp, cantidad)
        print(f"✅ Asignación insertada para territorio {numero}, conductor '{nombre_unificado}'")

    # ✅ cerrar bien
    cursor.close()
    conexion.close()

    guardar_errores_csv()
    print("\n🚀 Proceso finalizado")
