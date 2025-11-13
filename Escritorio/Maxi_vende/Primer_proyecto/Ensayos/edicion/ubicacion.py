from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.screen import MDScreen



class CustomListItem(OneLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Elemento con múltiples íconos"

        # Ícono a la izquierda
        self.add_widget(IconRightWidget(icon="account"))

        # Contenedor para múltiples íconos a la derecha
        icon_container = MDBoxLayout(
            adaptive_width=True, spacing="8dp", padding=("8dp", 0)
        )

        for icon_name in ["star", "pencil", "delete", "email", "alert"]:
            icon = IconRightWidget(icon=icon_name)
            icon.on_release = lambda x=icon_name: print(f"Clic en {x}")
            icon_container.add_widget(icon)

        self.add_widget(icon_container)


class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        screen = MDScreen()

        scroll = MDScrollView()
        mlist = MDList()

        # Agregamos múltiples ítems
        for _ in range(10):
            mlist.add_widget(CustomListItem())

        scroll.add_widget(mlist)
        screen.add_widget(scroll)
        return screen


MyApp().run()
