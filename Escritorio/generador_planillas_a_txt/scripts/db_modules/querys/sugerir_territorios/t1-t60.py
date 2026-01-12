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

def obtener_ultimas_fechas():
    """
    Devuelve una lista de tuplas:
    (numero_territorio, fecha_completado_última)
    """
    conexion = None
    cursor = None

    try:
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True)

        sql = """
        SELECT 
            t.numero,
            MAX(a.fecha_completado) AS ultima_fecha
        FROM Territorios t
        LEFT JOIN Asignaciones a ON a.territorio_id = t.id
        GROUP BY t.numero
        ORDER BY t.numero ASC;
        """

        cursor.execute(sql)
        filas = cursor.fetchall()

        datos = []
        for fila in filas:
            numero = fila["numero"]
            fecha = fila["ultima_fecha"]

            # Si nunca se hizo → pushear None
            if fecha is None:
                datos.append((numero, None))
            else:
                datos.append((numero, datetime.strptime(str(fecha), "%Y-%m-%d")))

        return datos

    except Error as e:
        print("❌ Error MySQL:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def mostrar_territorios_mas_atrasados(top=11):
    datos = obtener_ultimas_fechas()

    # Los que nunca se completaron → van primeros (más atrasados)
    datos_ordenados = sorted(
        datos,
        key=lambda x: x[1] if x[1] is not None else datetime.min
    )

    print("\n📌 **TOP Territorios más atrasados** (basado en fecha_completado)")
    print("-" * 55)

    contador = 0
    for numero, fecha in datos_ordenados:
        if contador >= top:
            break

        fecha_txt = fecha.strftime("%Y-%m-%d") if fecha else "NUNCA HECHO"
        print(f"  ▶ Territorio {numero:>2} — Última vez: {fecha_txt}")

        contador += 1

    print("-" * 55)


if __name__ == "__main__":
    mostrar_territorios_mas_atrasados(11)
