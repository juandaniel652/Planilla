class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def calcular_total(self):
        return self.precio * self.cantidad

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad
        }
