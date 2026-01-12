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

def eliminar_asignacion():
    print("=== ELIMINAR ASIGNACIÓN ESPECÍFICA ===")

    # --- Pedir datos al usuario ---
    conductor = input("Nombre del conductor (ej: Ortiz Aureliano): ").strip()
    fecha_asignado = input("Fecha asignado (YYYY-MM-DD): ").strip()
    fecha_completado = input("Fecha completado (YYYY-MM-DD): ").strip()
    territorio = input("Número de territorio: ").strip()
    cantidad = input("Cantidad abarcado (opcional, presiona Enter para saltar): ").strip()

    try:
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)

        # --- Buscar la asignación ---
        query = """
            SELECT a.id, c.nombre_completo, t.numero AS territorio,
                   a.fecha_asignado, a.fecha_completado, a.cantidad_abarcado
            FROM Asignaciones a
            JOIN Conductores c ON a.conductor_id = c.id
            JOIN Territorios t ON a.territorio_id = t.id
            WHERE c.nombre_completo = %s
              AND a.fecha_asignado = %s
              AND a.fecha_completado = %s
              AND t.numero = %s
        """

        params = [conductor, fecha_asignado, fecha_completado, territorio]

        if cantidad:
            query += " AND a.cantidad_abarcado = %s"
            params.append(cantidad)

        cursor.execute(query, params)
        resultados = cursor.fetchall()

        if not resultados:
            print("\n❌ No se encontró ninguna asignación con esos datos.")
            return

        # --- Mostrar coincidencias ---
        print("\nCoincidencias encontradas:")
        for fila in resultados:
            print(f"ID: {fila['id']} | Conductor: {fila['nombre_completo']} | "
                  f"Territorio: {fila['territorio']} | Asignado: {fila['fecha_asignado']} | "
                  f"Completado: {fila['fecha_completado']} | Cantidad: {fila['cantidad_abarcado']}")

        # --- Confirmar eliminación ---
        confirm = input("\n¿Eliminar esta(s) asignación(es)? (s/N): ").strip().lower()

        if confirm != 's':
            print("Operación cancelada.")
            return

        # --- Borrar ---
        ids = tuple(fila["id"] for fila in resultados)
        delete_query = "DELETE FROM Asignaciones WHERE id IN %s"

        cursor.execute(delete_query, (ids,))
        conn.commit()

        print("\n✔️ Asignación(es) eliminada(s) correctamente.")

    except Error as e:
        print("Error:", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    eliminar_asignacion()
