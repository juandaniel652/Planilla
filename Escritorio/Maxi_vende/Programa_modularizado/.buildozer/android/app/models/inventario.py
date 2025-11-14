from .producto import Producto

class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, nombre, precio, cantidad):
        nuevo = Producto(nombre, precio, cantidad)
        self.productos.append(nuevo)

    def calcular_total(self):
        return sum(p.calcular_total() for p in self.productos)

    def obtener_productos(self):
        return self.productos
