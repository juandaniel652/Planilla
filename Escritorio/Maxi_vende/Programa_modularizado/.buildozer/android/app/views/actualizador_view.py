from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar
from kivy.clock import Clock
from actualizaciones.actualizaciones import Actualizador
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivymd.icon_definitions import md_icons
from kivy.uix.widget import Widget


class ActualizadorView :

    def __init__ (self, app) :
        
        self.app = app
        self.dialog = None
        self.progress_bar = None
        self.actualizador = Actualizador()

    def verificar_actualizacion(self):
        info = self.actualizador.verificar_actualizacion()
        if info:
            self.mostrar_dialogo_confirmacion(info["version"])
        else:
            self.mostrar_dialogo_simple("✔ La aplicación ya está actualizada.")
            

    def mostrar_dialogo_confirmacion(self, nueva_version):

        # Tarjeta principal del diálogo
        card = MDCard(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(24),
            size_hint_y=None,
            adaptive_height=True,
            md_bg_color=(1, 1, 1, 1),
            radius=[20, 20, 20, 20],
            elevation=12,
        )

        # Icono grande y centrado
        icon_label = MDLabel(
            text=md_icons["update"],
            font_style="Icon",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 200 / 255, 83 / 255, 1),
            font_size="72sp",
            size_hint_y=None,
            height=dp(72),
        )

        # Mensaje centrado
        mensaje_label = MDLabel(
            text=f"[b]Nueva versión disponible[/b]\n\n[b]v{nueva_version}[/b]\n\n¿Deseas descargarla ahora?",
            markup=True,
            halign="center",
            valign="middle",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None,
            size_hint_x=1,
            height=dp(100),
            text_size=(dp(280), None),  # Ancho aproximado para centrado correcto
        )

        # Layout horizontal para los botones
        botones_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(16),
            size_hint_y=None,
            height=dp(48),
        )

        # Botón Cancelar
        boton_cancelar = MDRaisedButton(
            text="Cancelar",
            text_color="#FFFFFF",
            md_bg_color="#00C853",
            size_hint=(None, None),
            size=(dp(130), dp(48)),
            on_release=lambda x: self.dialog.dismiss(),
            elevation=6,
        )

        # Botón Actualizar
        boton_actualizar = MDRaisedButton(
            text="Actualizar",
            text_color="#FFFFFF",
            md_bg_color="#00C853",
            size_hint=(None, None),
            size=(dp(130), dp(48)),
            on_release=lambda x: self.iniciar_descarga(),
            elevation=6,
        )

        # Añadimos espaciadores para centrar los botones
        botones_layout.add_widget(Widget())  # Espaciador izquierdo
        botones_layout.add_widget(boton_cancelar)
        botones_layout.add_widget(boton_actualizar)
        botones_layout.add_widget(Widget())  # Espaciador derecho

        # Agregamos todo al card
        card.add_widget(icon_label)
        card.add_widget(mensaje_label)
        card.add_widget(botones_layout)

        # Creamos y mostramos el diálogo
        self.dialog = MDDialog(
            type="custom",
            content_cls=card,
            radius=[20, 20, 20, 20],
            elevation=12,
        )
        self.dialog.open()


    def iniciar_descarga(self):
        self.dialog.dismiss()
        layout = MDBoxLayout(orientation="vertical", spacing="12dp", padding="20dp")
        label = MDLabel(text="Descargando actualización...", halign="center")
        self.progress_bar = MDProgressBar(value=0, max=100)

        layout.add_widget(label)
        layout.add_widget(self.progress_bar)

        self.dialog = MDDialog(
            title="Descarga en curso",
            type="custom",
            content_cls=layout,
            buttons=[]
        )
        self.dialog.open()

        self.actualizador.descargar_apk(
            progreso_callback=self.actualizar_barra_progreso,
            completado_callback=self.finalizar_descarga
        )

    def actualizar_barra_progreso(self, porcentaje):
        if self.progress_bar:
            self.progress_bar.value = porcentaje

    def finalizar_descarga(self):
        self.dialog.dismiss()
        self.mostrar_dialogo_simple("✅ Descarga completa.\nInstalando nueva versión...")
        Clock.schedule_once(lambda dt: self.actualizador.instalar_apk(), 2)



    def mostrar_dialogo_simple (self, mensaje) :

        layout = MDBoxLayout(orientation="vertical", padding="20dp")

        layout.add_widget(MDLabel(text=mensaje, halign="center"))
        
        self.dialog = MDDialog(
            title="Actualización",
            type="custom",
            content_cls=layout,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss(), 
                text_color='#FFFFFF',
                md_bg_color='#00C853',
                font_name="Ancizar_botones",
                theme_text_color="Custom")
                
            ]
        )

        self.dialog.open()