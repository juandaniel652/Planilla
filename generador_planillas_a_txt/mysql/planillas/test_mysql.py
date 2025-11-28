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
        (41, 'Nahuel Benitez', '2023-03-19', '2023-03-24', 'Completo') ,
        (41, 'Juan Ontiveros', '2023-04-16', '2023-04-18', 'a, b') ,
        (41, 'Walter Valiente', '2023-05-07', '2023-05-14', 'Completo') ,
        (41, 'Juan Ontiveros', '2023-07-30', '2023-08-01', 'b, c') ,
        (41, 'L. Benitez', '2023-09-24', '2023-09-30', 'Completo') ,
        (42, 'Nahuel Benitez', '2023-04-23', '2023-04-29', 'Completo') ,
        (42, 'Fernando Israelson', '2023-07-16', '2023-07-23', 'a, b') ,
        (42, 'Nahuel Benitez', '2023-11-12', '2023-11-18', 'Completo') ,
        (42, 'Luis Benitez', '2024-05-05', '2024-05-12', 'Completo') ,
        (42, 'J. Argüello', '2024-09-15', '2024-09-22', 'Completo') ,
        (43, 'Joel Dominguez', '2023-06-18', '2023-06-24', 'd') ,
        (43, 'Joel Dominguez', '2023-09-17', '2023-09-23', 'Completo') ,
        (43, 'H. Altamirano', '2023-12-10', '2023-12-16', 'b, c') ,
        (43, 'Nahuel Benitez', '2023-12-17', '2023-12-23', 'd') ,
        (43, 'F. Israelson', '2024-01-07', '2024-01-14', 'Completo') ,
        (44, 'Nahuel Benitez', '2023-06-02', '2023-06-08', 'Completo') ,
        (44, 'Nahuel Benitez', '2023-12-17', '2024-12-23', 'Completo') ,
        (44, 'Juan Domínguez', '2024-12-22', '2024-12-28', 'Completo') ,
        (44, 'Walter Valiente', '2025-08-03', '2025-08-09', 'Completo') ,
        (45, 'Fernando Israelson', '2023-07-16', '2023-07-23', 'Completo') ,
        (45, 'Horacio Altamirano', '2023-12-10', '2023-12-16', 'a') ,
        (45, 'Fernando Israelson', '2025-01-19', '2025-01-25', 'Completo') ,
        (45, 'Walter Valiente', '2025-08-03', '2025-08-09', 'Completo') ,
        (46, 'Walter Valiente', '2023-07-23', '2023-07-30', 'Completo') ,
        (46, 'Horacio Altamirano', '2024-01-14', '2024-01-21', 'Completo') ,
        (46, 'Joel Domínguez', '2025-02-09', '2025-02-15', 'a, b') ,
        (46, 'Fernando Israelson', '2025-08-10', '2025-08-16', 'Completo') ,
        (47, 'Walter Valiente', '2023-07-16', '2023-07-22', 'Completo') ,
        (47, 'Walter Valiente', '2024-01-07', '2024-01-13', 'Completo') ,
        (47, 'F. Israelson', '2025-01-19', '2025-01-25', 'a-c') ,
        (47, 'Juan Domínguez', '2025-02-02', '2025-02-08', 'Completo') ,
        (47, 'F.Israelson', '2025-08-10', '2025-08-16', 'd') ,
        (48, 'Luis Benitez', '2023-03-26', '2023-04-02', 'a') ,
        (48, 'Joel Dominguez', '2023-04-09', '2023-04-15', 'Completo') ,
        (48, 'Nahuel Benitez', '2024-01-21', '2024-01-27', 'Completo') ,
        (49, 'Juan Ontiveros', '2023-03-26', '2023-04-02', 'Completo') ,
        (49, 'Horacio Altamirano', '2023-04-09', '2023-04-16', 'Completo') ,
        (49, 'Fernando Israelson', '2023-08-06', '2023-08-12', 'Completo') ,
        (49, 'Luis Benitez', '2024-05-12', '2024-05-19', 'Completo') ,
        (49, 'Joel Dominguez', '2024-12-22', '2024-12-29', 'e,f') ,
        (50, 'Luis Benitez', '2023-03-26', '2023-04-02', 'Completo') ,
        (50, 'Fernando Israelson', '2023-08-06', '2023-08-12', 'Completo') ,
        (50, 'Walter Valiente', '2024-06-02', '2024-06-09', 'Completo') ,
        (50, 'Gerardo Encina', '2024-08-04', '2024-08-11', 'Completo') ,
        (51, 'W. Valiente', '2023-03-05', '2023-03-11', 'b') ,
        (51, 'Horacio Altamirano', '2023-09-17', '2023-09-24', 'Completo') ,
        (51, 'Walter Valiente', '2023-10-08', '2023-10-15', 'Completo') ,
        (51, 'Gerardo Encina', '2024-08-04', '2024-08-11', 'Completo') ,
        (51, 'J. Ontiveros', '2024-09-01', '2024-09-08', 'b') ,
        (52, 'J. Ontiveros', '2023-03-26', '2023-04-02', 'c') ,
        (52, 'H. Altamirano', '2023-04-09', '2023-04-16', 'c') ,
        (52, 'Horacio Altamirano', '2023-09-17', '2023-09-24', 'Completo') ,
        (52, 'Joel Domínguez', '2024-12-22', '2024-12-29', 'Completo') ,
        (53, 'W. Valiente', '2023-03-05', '2023-03-11', 'a') ,
        (53, 'Luis Benitez', '2023-05-07', '2023-05-13', 'Completo') ,
        (53, 'Horacio Altamirano', '2023-11-26', '2023-12-02', 'Completo') ,
        (53, 'Maximiliano Coronel', '2024-08-11', '2024-08-18', 'Completo') ,
        (53, 'J. Ontiveros', '2024-09-01', '2024-09-08', 'a') ,
        (54, 'N. Benitez', '2023-03-05', '2023-03-12', 'a, b') ,
        (54, 'H. Altamirano', '2023-07-30', '2023-08-05', 'b') ,
        (54, 'Juan Ontiveros', '2024-09-01', '2024-09-08', 'Completo') ,
        (55, 'N. Benitez', '2023-03-05', '2023-03-12', 'a') ,
        (55, 'Horacio Altamirano', '2023-06-25', '2023-07-02', 'Completo') ,
        (55, 'Nahuel Benítez', '2024-09-29', '2024-10-05', 'Completo') ,
        (55, 'Joel Domínguez', '2024-11-03', '2024-11-10', 'Completo') ,
        (55, 'J.Arguello', '2025-08-17', '2025-08-23', 'Completo') ,
        (56, 'N. Benitez', '2023-06-25', '2023-07-01', 'a, b') ,
        (56, 'Horacio Altamirano', '2023-06-25', '2023-07-02', 'Completo') ,
        (56, 'H. Altamirano', '2023-07-30', '2023-08-05', 'a, b') ,
        (56, 'Nahuel Benitez', '2024-03-31', '2024-04-06', 'a, b') ,
        (56, 'Juan Ontiveros', '2024-11-03', '2024-11-10', 'Completo') ,
        (57, 'Jorge Argüello', '2023-03-19', '2023-03-26', 'Completo') ,
        (57, 'Gerardo Encina', '2023-08-13', '2023-08-20', 'Completo') ,
        (57, 'Walter Valiente', '2024-09-29', '2024-10-06', 'Completo') ,
        (57, 'Walter Valiente', '2025-07-13', '2025-07-19', 'Completo') ,
        (57, 'W.Valiente', '2025-08-31', '2025-09-06', 'Completo') ,
        (58, 'Jorge Argüello', '2023-03-19', '2023-03-26', 'Completo') ,
        (58, 'Gerardo Encina', '2023-08-13', '2023-08-20', 'Completo') ,
        (58, 'Walter Valiente', '2024-09-29', '2024-10-06', 'Completo') ,
        (58, 'Joel Dominguez', '2025-03-30', '2025-04-05', 'Completo') ,
        (58, 'Walter Valiente', '2025-07-13', '2025-07-19', 'Completo') ,
        (59, 'Jorge Argüello', '2023-03-19', '2023-03-26', 'Completo') ,
        (59, 'Horacio Altamirano', '2023-07-30', '2023-08-06', 'Completo') ,
        (59, 'Walter Valiente', '2024-09-29', '2024-10-06', 'Completo') ,
        (59, 'Nahuel Benítez', '2025-03-16', '2025-03-22', 'Completo') ,
        (59, 'Joel Dominguez', '2025-05-25', '2025-05-31', 'Completo') ,
        (60, 'J. Argüello', '2023-03-19', '2023-03-26', 'a, c, d') ,
        (60, 'H. Altamirano', '2023-07-30', '2023-08-06', 'a, b') ,
        (60, 'G. Encina', '2023-08-13', '2023-08-20', 'c, d') ,
        (60, 'Walter Valiente', '2024-09-29', '2024-10-06', 'Completo') ,
        (60, 'N. Benítez', '2025-03-16', '2025-03-22', 'Completo') ,
        (41, 'Juan Ontiveros', '2023-11-05', '2023-11-11', 'b, c') ,
        (41, 'Juan Ontiveros', '2023-11-19', '2023-11-25', 'a') ,
        (41, 'Walter Valiente', '2023-12-24', '2023-12-30', 'Completo') ,
        (41, 'Juan Dominguez', '2024-03-03', '2024-03-09', 'Completo') ,
        (41, 'H. Altamirano', '2024-06-30', '2024-07-07', 'Completo') ,
        (42, 'Juan Domínguez', '2025-02-02', '2025-02-08', 'c') ,
        (43, 'Jorge Argüello', '2024-09-15', '2024-09-22', 'Completo') ,
        (43, 'Claudio Crocco', '2025-07-07', '2025-07-12', 'Completo') ,
        (51, 'Jorge Cardozo', '2025-03-30', '2025-04-05', 'Completo') ,
        (55, 'Walter Valiente', '2025-11-16', '2025-11-22', 'Completo') ,
        (56, 'Joel Domínguez', '2025-01-05', '2025-01-12', 'Completo') ,
        (56, 'D. Ferreyra', '2025-04-27', '2025-05-04', 'a, b') ,
        (56, 'Jorge Argüello', '2025-08-17', '2025-08-23', 'b,c') ,
        (56, 'Walter Valiente', '2025-11-16', '2025-11-22', 'Completo') ,
        (57, 'Walter Valiente', '2025-11-16', '2025-11-22', 'Completo') ,
        (58, 'Walter Valiente', '2025-08-31', '2025-09-06', 'Completo') ,
        (59, 'Walter Valiente', '2025-08-31', '2025-09-06', 'Completo') ,
        (60, 'Walter Valiente', '2025-07-13', '2025-07-19', 'c') ,
        (60, 'Walter Valiente', '2025-08-31', '2025-09-06', 'Completo') ,
        (41, 'A. Domínguez', '2025-03-16', '2025-03-20', 'Completo') ,
        (41, 'Luis Benítez', '2025-03-23', '2025-03-28', 'Completo') ,
        (41, 'Walter Valiente', '2025-05-18', '2025-05-24', 'Completo') ,
        (41, 'Claudio Crocco', '2025-07-07', '2025-07-12', 'Completo') ,
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
