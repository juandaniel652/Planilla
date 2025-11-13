from kivymd.app import MDApp
from views.main_view import MainApp
from fuentes.fuentes_disponibles import registrar_fuentes


class AppVentas (MDApp) :

    icon = 'images/carrito_compras.png'

    def build(self) :

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"  
        registrar_fuentes()  
        return MainApp()


if __name__ == "__main__" :

    AppVentas().run()
