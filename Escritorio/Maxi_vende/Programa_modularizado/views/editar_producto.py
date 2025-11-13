from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, NumericProperty

class EditarProducto(MDBoxLayout):
    nombre = StringProperty("")
    precio = NumericProperty(0)
    cantidad = NumericProperty(0)
