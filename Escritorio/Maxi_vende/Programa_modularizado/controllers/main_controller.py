from models.producto import Producto
from models.inventario import Inventario
from persistencia.persistencia import guardar_productos_temp
from persistencia.persistencia import cargar_productos_temp
from persistencia.persistencia import eliminar_productos_temp
from models.producto import Producto


class MainController:
    def __init__(self, vista):
        self.vista = vista
        self.inventario = Inventario()

    def agregar_producto(self, nombre, precio, cantidad):
        self.inventario.agregar_producto(nombre, precio, cantidad)
        self.vista.actualizar_lista(self.inventario.obtener_productos())
        self.actualizar_persistencia()  # ← CAMBIO

    def obtener_total(self):
        return self.inventario.calcular_total()

    def aumentar_cantidad(self, index):
        self.inventario.productos[index].cantidad += 1
        self.vista.actualizar_lista(self.inventario.obtener_productos())
        self.actualizar_persistencia()  # ← CAMBIO

    def disminuir_cantidad(self, index):
        if self.inventario.productos[index].cantidad > 1:
            self.inventario.productos[index].cantidad -= 1
            self.vista.actualizar_lista(self.inventario.obtener_productos())
            self.actualizar_persistencia()  # ← CAMBIO

    def actualizar_persistencia(self):
        productos = self.inventario.obtener_productos()
        lista_dicts = [p.to_dict() for p in productos]
        guardar_productos_temp(lista_dicts)

    def cargar_datos_previos(self):
        productos = cargar_productos_temp()
        for prod in productos:
            self.inventario.agregar_producto(prod["nombre"], prod["precio"], prod["cantidad"])

    def guardar_ganancia(self):
        self.inventario.guardar_en_db()
        eliminar_productos_temp()




