import mysql.connector
from mysql.connector import Error
from datetime import datetime

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="miclave123",
        database="Planillas",
        ssl_disabled=True
    )

def obtener_id_territorio(numero, cursor):
    cursor.execute("SELECT id FROM Territorios WHERE numero = %s", (numero,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"❌ Territorio lógico {numero} no existe.")
    return row["id"]

def mostrar_asignaciones_territorio(numero_territorio):
    conexion = None
    cursor = None

    try:
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True)

        sql = """
        SELECT 
            c.nombre_completo AS conductor,
            a.fecha_asignado,
            a.fecha_completado,
            a.cantidad_abarcado
        FROM Asignaciones a
        JOIN Territorios t ON a.territorio_id = t.id
        JOIN Conductores c ON a.conductor_id  = c.id
        WHERE t.numero = %s;
        """

        cursor.execute(sql, (numero_territorio,))
        filas = cursor.fetchall()

        if not filas:
            print(f"⚠️ No hay asignaciones para territorio {numero_territorio}")
            return

        # Ordenar por fecha asignada más antigua → más reciente
        filas.sort(
            key=lambda f: datetime.strptime(str(f["fecha_asignado"]), "%Y-%m-%d") if f["fecha_asignado"] else datetime.max
        )

        print(f"\n📌 Asignaciones — Territorio {numero_territorio} (orden cronológico)")
        print("-" * 65)

        for fila in filas:
            print(f"   Conductor: {fila['conductor']}")
            print(f"   Fecha Asignado:   {fila['fecha_asignado'] or '—'}")
            print(f"   Fecha Completado: {fila['fecha_completado'] or '—'}")
            print(f"   Territorios:     {fila['cantidad_abarcado'] or '—'}")
            print()

        print("-" * 65)

    except Error as e:
        print(f"❌ Error MySQL:", e)

    except ValueError as ve:
        print(ve)

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

if __name__ == "__main__":
    
    while True:
        num = input("Ingrese número del territorio a consultar (-1 para salir): ").strip()
        if num == "-1":
            print("Saliendo.")
            break
        if num.isdigit():
            mostrar_asignaciones_territorio(int(num))
        else:
            print("❌ Debe ingresar un número válido o -1 para salir.")
