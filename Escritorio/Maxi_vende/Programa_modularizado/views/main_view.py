from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from controllers.main_controller import MainController
from views.editar_producto import EditarProducto
from database.database import RegistroVenta
from datetime import datetime
from views.dialogs import HistorialDialog
from views.actualizador_view import ActualizadorView
from models.producto import Producto
from utils.ventana_emergente import crear_caja_emergente


Builder.load_file("views/main_view.kv")


class ProductoItem (OneLineAvatarIconListItem) :

    nombre = StringProperty()
    precio = NumericProperty()
    cantidad = NumericProperty()
    index = NumericProperty()



class MainApp (MDBoxLayout) : 

    productos = ListProperty()
    total = NumericProperty(0)
    dialog = None
    producto_actual = None


    def __init__ (self, **kwargs) :

        super().__init__(**kwargs)
        self.controller = MainController(self)   


    def verificar_actualizacion (self) :

        if not hasattr(self, "actualizador_view") :

            self.actualizador_view = ActualizadorView(self)
        
        self.actualizador_view.verificar_actualizacion()


    def agregar_producto (self) :

        self._mostrar_editor(EditarProducto(), self._guardar_nuevo_producto)


    def editar_producto (self, index) :

        producto = self.productos[index]
        widget = EditarProducto(
            nombre=producto["nombre"],
            precio=producto["precio"],
            cantidad=producto["cantidad"]
        )
        self.producto_actual = index
        self._mostrar_editor(widget, self._guardar_edicion_producto)


    def _guardar_nuevo_producto (self, *args) :

        datos = self._leer_datos_editor()
        self.controller.agregar_producto(*datos)
        self.dialog.dismiss()


    def _guardar_edicion_producto(self, *args) :
        
        nombre, precio, cantidad = self._leer_datos_editor()
        producto = self.controller.inventario.productos[self.producto_actual]
        producto.nombre = nombre
        producto.precio = precio
        producto.cantidad = cantidad

        self.actualizar_lista(self.controller.inventario.obtener_productos())
        self.dialog.dismiss()


    def _leer_datos_editor (self) :

        nombre = self.dialog.content_cls.ids.nombre.text
        precio = float(self.dialog.content_cls.ids.precio.text or 0)
        cantidad = int(self.dialog.content_cls.ids.cantidad.text or 0)
        return nombre, precio, cantidad


    def _mostrar_editor (self, widget, accion_confirmar) :

        self.dialog = MDDialog(
            title="Producto",
            type="custom",
            content_cls=widget,
            buttons=[
                MDRaisedButton(text="CANCELAR", 
                                on_release=lambda x: self.dialog.dismiss(),
                                text_color='#FFFFFF',
                                md_bg_color='#00C853',
                                font_name="Ancizar_botones",
                                theme_text_color="Custom"),

                MDRaisedButton (text="GUARDAR", 
                                on_release=accion_confirmar, 
                                text_color='#FFFFFF',
                                md_bg_color='#00C853',
                                font_name="Ancizar_botones",
                                theme_text_color="Custom"),
            ],
        )
        self.dialog.open()


    def actualizar_lista (self, productos) :

        self.ids.productos_layout.clear_widgets()
        self.productos = []
        for i, p in enumerate(productos):
            item = ProductoItem(
                text=f"      {p.nombre} - ${p.precio:.2f} x {p.cantidad}",
                nombre=p.nombre,
                precio=p.precio,
                cantidad=p.cantidad,
                index=i
            )
            self.ids.productos_layout.add_widget(item)
            self.productos.append({
                "nombre": p.nombre,
                "precio": p.precio,
                "cantidad": p.cantidad
            })

        self.total = self.controller.obtener_total()


    def aumentar_cantidad (self, index) :

        self.controller.aumentar_cantidad(index)


    def disminuir_cantidad (self, index) :

        self.controller.disminuir_cantidad(index)


    def eliminar_producto(self, index) :

        del self.productos[index]
        self.actualizar_lista(self._convertir_a_objetos())


    def _convertir_a_objetos(self):
        
        return [Producto(producto["nombre"], producto["precio"], producto["cantidad"]) for producto in self.productos]


    def guardar_ganancia (self) :

        try : 

            productos = self.controller.inventario.obtener_productos()

            if not productos :

                print("No hay productos para guardar.")
                crear_caja_emergente("Vacío", "No hay productos para guardar")
                return

            for producto in productos :

                venta = RegistroVenta(producto.nombre, producto.precio, producto.cantidad)
                venta.guardar()

            print("Ganancia guardada correctamente.")
            crear_caja_emergente("Mensaje", "Ganancia guardada en la base de datos.")

            # Opcional: limpiar la lista después de guardar
            self.controller.inventario.productos.clear()
            self.actualizar_lista([])

        except : 

            crear_caja_emergente("Error", "No se pudo guardar la ganancia en la base de datos.")


    def mostrar_historial (self) :
        
        HistorialDialog(self).mostrar_meses()
