#Agrega datos a la Base  (lo que se va llenando semana por semana)
import mysql.connector
from mysql.connector import Error

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="miclave123",
        database="Planillas",
        ssl_disabled=True
    )

def obtener_id_territorio(numero_territorio, cursor):
    cursor.execute("SELECT id FROM Territorios WHERE numero = %s", (numero_territorio,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"❌ Territorio {numero_territorio} no existe en la tabla Territorios")
    return row[0]

def insertar_asignacion(territorio_num, nombre, fecha_asig, fecha_comp, alias):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        terr_id = obtener_id_territorio(territorio_num, cursor)

        sql = """
        INSERT INTO Asignaciones (territorio_id, conductor_id, fecha_asignado, fecha_completado, cantidad_abarcado)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (terr_id, nombre, fecha_asig, fecha_comp, alias))
        conexion.commit()

        print(f"✅ Asignación insertada en territorio {territorio_num} (ID real {terr_id})")

    except (Error, ValueError) as e:
        print(e)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# ----------------------------------------------------------------
# Insertar muchas tuplas en cualquier orden:
# ----------------------------------------------------------------

asignaciones = [
    (2, 'Ortiz Aureliano', '2025-11-16', '2025-11-17', '(b,c)'),
    (2, 'Cristian Viera', '2025-11-30', '2025-12-02', 'Completo')
]

for a in asignaciones:
    insertar_asignacion(*a)
