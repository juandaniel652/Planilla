from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

KV = '''
ScrollView:
    do_scroll_x: False
    do_scroll_y: True

    GridLayout:
        id: grid
        cols: 4
        size_hint_y: None
        height: self.minimum_height
        row_default_height: '80dp'
        row_force_default: True
        padding: dp(10)
        spacing: dp(10)
'''

class MyApp(MDApp):
    def build(self):
        root = Builder.load_string(KV)
        grid = root.ids.grid

        for i in range(100):
            grid.add_widget(
                Label(
                    text=f"Elemento {i}",
                    size_hint_y=None,
                    height='80dp'
                )
            )

        return root

MyApp().run()
