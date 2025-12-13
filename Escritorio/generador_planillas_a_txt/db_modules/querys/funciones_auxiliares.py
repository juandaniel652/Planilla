import unicodedata
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
    
def normalizar_texto(texto):
    """
    Convierte el texto a minúsculas y elimina acentos/caracteres especiales.
    Ej: 'Ortíz Aureliano' -> 'ortiz aureliano'
    """
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join([c for c in texto if not unicodedata.combining(c)])
    return texto.strip()

def obtener_id_conductor(nombre, cursor):
    """
    Busca el ID del conductor por nombre, aplicando normalización.
    """
    nombre_norm = normalizar_texto(nombre)
    cursor.execute("SELECT id, nombre_completo FROM Conductores")
    rows = cursor.fetchall()

    for row in rows:
        id_conductor, nombre_db = row
        if normalizar_texto(nombre_db) == nombre_norm:
            return id_conductor

    raise ValueError(f"❌ Conductor '{nombre}' no existe en la tabla Conductores")

def obtener_id_territorio(numero_territorio, cursor):
    """
    Busca el ID del territorio por número.
    """
    cursor.execute("SELECT id FROM Territorios WHERE numero = %s", (numero_territorio,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"❌ Territorio {numero_territorio} no existe en la tabla Territorios")
    return row[0]


if __name__ == '__main__' : 
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        id_conductor = obtener_id_conductor("Juan Dominguez", cursor)  # Prueba rápida
        print(f"ID del conductor encontrado: {id_conductor}")
        
        cursor.close()
        conexion.close()
    except ValueError as e:
        print(e)
    except Error as e:
        print(f"Error de conexión: {e}")
    
    