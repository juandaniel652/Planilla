from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.uix.label import Label

def mostrar_historial_bottomsheet(self):
    from kivy.lang import Builder
    content = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height

    ScrollView:
        GridLayout:
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            id: historial_grid
''')

    for i in range(30):
        content.ids.historial_grid.add_widget(Label(text=f"Registro {i}", size_hint_y=None, height=30))

    self.bottom_sheet = MDCustomBottomSheet(screen=content)
    self.bottom_sheet.open()
