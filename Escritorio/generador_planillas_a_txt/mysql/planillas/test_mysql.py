#Tesea el mismo funcionamiento de "conexion_mysql.py" pero sin conectar a MySQL
import re
from datetime import datetime
import csv

# No importamos mysql porque es solo simulación en el test

errores = []

# --- MAPA DE NOMBRES INTELIGENTE ---
mapa_nombres = {
    r"^f\.?\s*israelson$": "Fernando Israelson",
    r"^fernando\s+israelson$": "Fernando Israelson",
    r"^ferando\s+israelson$": "Fernando Israelson",
    r"^a\.?\s*israelson$": "Fernando Israelson",
    r"^ju\.?\s*dominguez$": "Juan Domínguez",
    r"^juan\s+dominguez$": "Juan Domínguez",
    r"^j\.?\s*dom[ií]nguez$": "Joel Domínguez",
    r"^walter\s+valiente$": "Walter Valiente",
    r"^w\.?\s*valiente$": "Walter Valiente",
    r"^w\.?\s*valiente$": "Walter Valiente",
    r"^n\.?\s*ben[ií]tez$": "Nahuel Benítez",
    r"^nahuel\s+ben[ií]tez$": "Nahuel Benítez",
    r"^l(ui|u)\.?s?\s+ben[ií]tez$": "Luis Benítez",
    r"^l\.?\s*ben[ií]tez$": "Luis Benítez",
    r"^jorge\s+arg[üu]ello$": "Jorge Argüello",
    r"^j\.?\s*arg[üu]ello$": "Jorge Argüello",
}

def normalizar_nombre(nombre_original):
    nombre = nombre_original.lower().strip()
    for patron, canonico in mapa_nombres.items():
        if re.match(patron, nombre, flags=re.IGNORECASE):
            return canonico
    return nombre_original.title()

def validar_fechas(fecha_asig, fecha_comp):
    try:
        a = datetime.strptime(fecha_asig, "%Y-%m-%d")
        b = datetime.strptime(fecha_comp, "%Y-%m-%d")
        return not (b < a)
    except:
        return False

# ---- SIMULACIÓN EN MEMORIA ----
territorios_creados = set()
conductores_unificados = {}  # original → unificado

def simular_insert_asignacion(tupla):
    numero, nombre_orig, fecha_asig, fecha_comp, alias = tupla
    nombre_unificado = normalizar_nombre(nombre_orig)
    conductores_unificados[nombre_orig] = nombre_unificado

    if numero not in territorios_creados:
        territorios_creados.add(numero)
        print(f"📌 Nuevo territorio detectado → Se insertaría Territorio {numero}")

    if nombre_orig not in conductores_unificados:
        print(f"👤 Nuevo conductor → Se insertaría Conductor '{nombre_unificado}'")

    print(f"   ➤ Se insertaría en MySQL: ({numero}, '{nombre_unificado}', '{fecha_asig}', '{fecha_comp}', '{alias}')")

# ---- TEST PRINCIPAL ----
if __name__ == "__main__":

    print("\n🔍=== TEST DEL MÓDULO (SIN INSERTAR A MYSQL) ===\n")

    tuplas = [
        (10, 'Maximiliano Gomez', '2025-11-23', '2025-11-28', '(a-d)'),
        (11, 'Esteban Salas', '2025-11-23', '2025-11-26', 'Completo'),
        (14, 'Leandro Quiroz', '2025-11-30', '2025-12-04', 'b,c'),
        (15, 'Esteban Salas', '2025-11-23', '2025-11-25', 'a, b, c'),
        (18, 'Juan Herrera', '2025-11-30', '2025-12-04', 'Completo'),
        (19, 'Isabel Ontiveros', '2025-11-23', '2025-11-25', 'b,c'),
        (20, 'Jorge Arguello', '2025-11-23', '2025-11-24', 'Completo'),
    ]

    for numero, nombre, fecha_asig, fecha_comp, alias in tuplas:
        
        # Registrar conductor unificado
        nombre_unificado = normalizar_nombre(nombre)
        conductores_unificados[nombre] = nombre_unificado

        # Validar fechas
        if not validar_fechas(fecha_asig, fecha_comp):
            motivo = "Fecha inválida o fecha_completado < fecha_asignado"
            print(f"❌ ERROR detectado en fechas → Territorio {numero}, Nombre '{nombre}' ({fecha_asig} → {fecha_comp})")
            errores.append((numero, nombre, fecha_asig, fecha_comp, motivo))
            continue

        # Mostrar simulación de inserción
        simular_insert_asignacion((numero, nombre, fecha_asig, fecha_comp, alias))

    # Guardar informe
    with open("informe_errores.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["territorio", "nombre", "fecha_asig", "fecha_comp", "motivo"])
        writer.writerows(errores)

    print("\n📁 Se generaría informe_errores.csv con los errores detectados.")
    print("\n👥 Unificación de nombres realizada:")
    for orig, unif in conductores_unificados.items():
        print(f"   '{orig}' → '{unif}'")

    print("\n🚀 Test finalizado sin insertar en MySQL.\n")
