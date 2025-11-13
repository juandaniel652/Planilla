from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.screen import MDScreen
from kivy.uix.scrollview import ScrollView


class MyApp(MDApp):
    def build(self):
        self.screen = MDScreen()
        scroll = ScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        self.screen.add_widget(scroll)

        # Crear filas dinámicamente con funcionalidad
        for i in range(10):
            item = OneLineListItem(text=f"Elemento {i + 1}")
            item.bind(on_release=self.item_pressed)
            self.list_view.add_widget(item)

        return self.screen

    def item_pressed(self, instance):
        print(f"Se hizo clic en: {instance.text}")


MyApp().run()
