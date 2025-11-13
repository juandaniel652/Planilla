from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.clock import Clock

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.cambiar_a_main, 5)  # 2 segundos de carga

    def cambiar_a_main(self, dt):
        self.manager.current = 'main'

class MainScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MainScreen(name='main'))
        return sm


MyApp().run()