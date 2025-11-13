import sqlite3
from datetime import datetime

class RegistroVenta:
    def __init__(self, producto, precio, cantidad, fecha=None):
        self.producto = producto
        self.precio = precio
        self.cantidad = cantidad
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.total = round(precio * cantidad, 2)
        self.mes = self.fecha.split("-")[1]
        self.anio = self.fecha.split("-")[0]

    def guardar(self):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT,
                    precio REAL,
                    cantidad INTEGER,
                    fecha TEXT,
                    total REAL,
                    mes TEXT,
                    anio INTEGER
                )
            ''')
            cursor.execute('''
                INSERT INTO ventas (producto, precio, cantidad, fecha, total, mes, anio)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.producto, self.precio, self.cantidad, self.fecha, self.total, self.mes, self.anio))
            conn.commit()


class ConsultaVentas:
    @staticmethod
    def obtener_resumen_mes(mes, anio):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mes, anio, MAX(cantidad)
                FROM ventas
                WHERE mes = ? AND anio = ?
            """, (mes, anio))
            return cursor.fetchall()

    @staticmethod
    def obtener_totales_por_fecha(mes):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fecha, SUM(precio * cantidad) AS total_ventas
                FROM ventas
                WHERE mes = ?
                GROUP BY fecha
                ORDER BY fecha ASC
            """, (mes,))
            return cursor.fetchall()

    @staticmethod
    def obtener_detalles_por_fecha(fecha):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT producto, cantidad, precio, total
                FROM ventas
                WHERE fecha = ?
            """, (fecha,))
            return cursor.fetchall()

    @staticmethod
    def obtener_total_dia(fecha):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(precio * cantidad)
                FROM ventas
                WHERE fecha = ?
            """, (fecha,))
            return cursor.fetchone()[0] or 0

    @staticmethod
    def obtener_cantidad_total_dia(fecha):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(cantidad)
                FROM ventas
                WHERE fecha = ?
            """, (fecha,))
            return cursor.fetchone()[0] or 0


class ConsultaHistorial:

    @staticmethod
    def obtener_meses_y_anios():
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT mes, anio FROM ventas ORDER BY anio DESC, mes DESC")
            return cursor.fetchall()

    @staticmethod
    def obtener_fechas_de_mes(mes, anio):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT fecha
                FROM ventas
                WHERE mes = ? AND anio = ?
                ORDER BY fecha ASC
            """, (mes, anio))
            return [f[0] for f in cursor.fetchall()]

    @staticmethod
    def obtener_detalles_de_fecha(fecha):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT producto, cantidad, precio, total
                FROM ventas
                WHERE fecha = ?
            """, (fecha,))
            return cursor.fetchall()

    @staticmethod
    def obtener_totales_de_fecha(fecha):
        with sqlite3.connect("konta_venta.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(cantidad), SUM(total)
                FROM ventas
                WHERE fecha = ?
            """, (fecha,))
            return cursor.fetchone()

    @staticmethod
    def actualizar_producto_en_fecha(fecha, nombre_antiguo, nombre_nuevo, precio, cantidad):
        conexion = sqlite3.connect("konta_venta.db")
        cursor = conexion.cursor()
        total = precio * cantidad
        cursor.execute("""
            UPDATE ventas
            SET producto = ?, precio = ?, cantidad = ?, total = ?
            WHERE fecha = ? AND producto = ?
        """, (nombre_nuevo, precio, cantidad, total, fecha, nombre_antiguo))
        
        conexion.commit()
        conexion.close()

