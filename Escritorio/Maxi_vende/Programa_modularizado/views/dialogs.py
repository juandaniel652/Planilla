from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, MDList
from kivy.uix.scrollview import ScrollView
from database.database import ConsultaHistorial
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from kivymd.uix.label import MDIcon
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from functools import partial
from kivymd.uix.button import MDIconButton
from utils.validacion_historial import validar_campos_producto_edicion



MESES = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}

def formato_fecha (fecha_str) :

    try :

        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        dia = f"{fecha.day:02d}"
        mes = MESES[fecha.strftime("%m")]
        anio = fecha.year
        return f"{dia} de {mes} {anio}"
    
    except :

        return fecha_str


class DialogFactory:
    @staticmethod
    def crear_dialogo_confirmacion(titulo, texto, accion_si, accion_no=None):
        return MDDialog(
            title=titulo,
            text=texto,
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    on_release=accion_no if accion_no else lambda x: None
                ),
                MDFlatButton(
                    text="ACEPTAR",
                    on_release=accion_si
                ),
            ]
        )


class HistorialDialog:

    def __init__ (self, root) :

        self.root = root
        self.dialog = None


    def mostrar_meses (self) :

        layout = MDList()
        meses = ConsultaHistorial.obtener_meses_y_anios()

        if not meses :

            layout.add_widget(OneLineListItem(text="No hay meses registrados."))

        else :

            for mes, anio in meses :

                nombre_mes = MESES.get(mes.zfill(2), mes)
                item = OneLineListItem(
                    text=f"{nombre_mes} {anio}",
                    font_style="Subtitle1",
                    on_release=lambda x, m=mes, a=anio: self.mostrar_fechas(m, a)
                )
                layout.add_widget(item)

        scroll = ScrollView(size_hint=(1, None), size=(self.root.width, 300))
        scroll.add_widget(layout)

        # Título con ícono
        titulo_con_icono = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            padding=(dp(16), dp(16), dp(16), 0),
            adaptive_height=True
        )

        icono = MDIcon(icon="calendar-month", size_hint=(None, None), size=(dp(24), dp(24)))
        titulo = MDLabel(text="Historial de Ventas por Mes", font_style="H6", halign="left", theme_text_color="Primary")

        titulo_con_icono.add_widget(icono)
        titulo_con_icono.add_widget(titulo)

        contenedor = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True
        )

        contenedor.add_widget(titulo_con_icono)
        contenedor.add_widget(scroll)

        self.dialog = MDDialog(
            type="custom",
            content_cls=contenedor,
            buttons=[],
        )

        self.dialog.open()


    def mostrar_fechas(self, mes, anio):
    
        self.dialog.dismiss()

        layout = MDList()
        fechas = ConsultaHistorial.obtener_fechas_de_mes(mes, anio)

        if not fechas:
            layout.add_widget(OneLineListItem(text="No hay fechas registradas."))
        else:
            for fecha in fechas:
                fecha_formateada = formato_fecha(fecha)
                item = OneLineListItem(
                    text=f"{fecha_formateada}",
                    font_style="Subtitle1",
                    on_release=lambda x, f=fecha: self.mostrar_detalles(f)
                )
                layout.add_widget(item)

        scroll = ScrollView(size_hint=(1, None), size=(self.root.width, 300))
        scroll.add_widget(layout)

        # Título con ícono
        nombre_mes = MESES.get(mes.zfill(2), mes)
        titulo_con_icono = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            padding=(dp(16), dp(16), dp(16), 0),
            adaptive_height=True
        )

        icono = MDIcon(icon="calendar-range", size_hint=(None, None), size=(dp(24), dp(24)))
        titulo = MDLabel(text=f"Días de {nombre_mes} {anio}", font_style="H6", halign="left", theme_text_color="Primary")

        titulo_con_icono.add_widget(icono)
        titulo_con_icono.add_widget(titulo)

        contenedor = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True
        )
        contenedor.add_widget(titulo_con_icono)
        contenedor.add_widget(scroll)

        self.dialog = MDDialog(
            type="custom",
            content_cls=contenedor,
            buttons=[],
        )
        self.dialog.open()



    def mostrar_detalles(self, fecha):
        self.dialog.dismiss()

        detalles = ConsultaHistorial.obtener_detalles_de_fecha(fecha)
        total_cant, total_precio = ConsultaHistorial.obtener_totales_de_fecha(fecha)

        layout = MDBoxLayout(
            orientation='vertical',
            spacing='12dp',
            padding=('12dp', '12dp', '12dp', '12dp'),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))

        if detalles:
            for prod, cant, precio, tot in detalles:
                #
                icono_editar = MDIconButton(
                    icon="pencil",
                    icon_size="24sp",
                    theme_text_color="Custom",
                    text_color=(0.1, 0.5, 0.9, 1),
                    on_release=partial(self.abrir_dialog_edicion, (prod, cant, precio, tot), fecha)
                )

                top_row = MDBoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height="30dp",
                    spacing="8dp"
                )
                top_row.add_widget(MDLabel(
                    text=f"[b]{prod}[/b]",
                    markup=True,
                    font_style="Subtitle1",
                    theme_text_color="Primary",
                    halign="left"
                ))
                top_row.add_widget(icono_editar)

                card_layout = MDBoxLayout(
                    orientation="vertical",
                    spacing="6dp"
                )
                card_layout.add_widget(top_row)
                card_layout.add_widget(MDLabel(
                    text=f"{cant} x ${precio:.2f} = ${tot:.2f}",
                    font_style="Body2",
                    theme_text_color="Secondary",
                    halign="left"
                ))

                card = MDCard(
                    orientation="vertical",
                    size_hint=(1, None),
                    height="110dp",
                    padding="12dp",
                    radius=[16, 16, 16, 16],
                    md_bg_color=(1, 1, 1, 1),
                    shadow_softness=2,
                    shadow_offset=(0, 2),
                    ripple_behavior=True,
                    style="elevated"
                )
                card.add_widget(card_layout)
                layout.add_widget(card)

            layout.add_widget(MDLabel(
                text=f"[b]Total cantidad:[/b] {total_cant}",
                markup=True,
                font_style="Subtitle2",
                theme_text_color="Custom",
                text_color=(0.2, 0.6, 0.2, 1),
                halign="right"
            ))
            layout.add_widget(MDLabel(text="", size_hint_y=None, height="8dp"))
            layout.add_widget(MDLabel(
                text=f"[b]Total precio:[/b] ${total_precio:.2f}",
                markup=True,
                font_style="Subtitle2",
                theme_text_color="Custom",
                text_color=(0.2, 0.6, 0.2, 1),
                halign="right"
            ))

        else:
            layout.add_widget(MDLabel(
                text="No se encontraron ventas para esta fecha.",
                theme_text_color="Hint",
                halign="center",
                font_style="Body1"
            ))

        scroll = ScrollView(
            size_hint=(1, None),
            size=(self.root.width, min(self.root.height * 0.7, 500))
        )
        scroll.add_widget(layout)

        self.dialog = MDDialog(
            title=f"Ventas del {fecha}",
            type="custom",
            radius=[20, 20, 20, 20],
            content_cls=scroll,
            buttons=[]
        )
        self.dialog.open()


    
    def abrir_dialog_edicion(self, producto, fecha, *args):
        nombre, cantidad, precio, _ = producto
        self.producto_editado = producto

        nombre_field = MDTextField(
            text=nombre,
            hint_text="Nombre",
            mode="rectangle",
            size_hint_x=1,
            font_name="Ancizar_contenido",
            font_size="18sp"
        )
        precio_field = MDTextField(
            text=str(precio),
            hint_text="Precio",
            input_filter="float",
            mode="rectangle",
            size_hint_x=1,
            font_name="Ancizar_contenido",
            font_size="18sp"
        )
        cantidad_field = MDTextField(
            text=str(cantidad),
            hint_text="Cantidad",
            input_filter="int",
            mode="rectangle",
            size_hint_x=1,
            font_name="Ancizar_contenido",
            font_size="18sp"
        )

        self.campos_edicion = {
            "nombre": nombre_field,
            "precio": precio_field,
            "cantidad": cantidad_field
        }

        def validar_y_guardar(fecha):
            nombre_val = nombre_field.text
            precio_val = precio_field.text
            cantidad_val = cantidad_field.text

            if validar_campos_producto_edicion(nombre_val, precio_val, cantidad_val):
                self.edit_dialog.dismiss()
                self.guardar_edicion_producto(fecha)

        card_contenido = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            adaptive_height=True
        )
        card_contenido.add_widget(nombre_field)
        card_contenido.add_widget(precio_field)
        card_contenido.add_widget(cantidad_field)

        botones_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=(0, dp(8)),
            size_hint_y=None,
            height=dp(52),
            pos_hint={"center_x": 0.5}
        )
        botones_layout.add_widget(
            MDRaisedButton(
                text="Cancelar",
                on_release=lambda x: self.edit_dialog.dismiss(),
                text_color='#FFFFFF',
                md_bg_color='#00C853',
                font_name="Ancizar_botones",
                theme_text_color="Custom"
            )
        )
        botones_layout.add_widget(
            MDRaisedButton(
                text="Guardar",
                on_release=lambda x: validar_y_guardar(fecha),
                text_color='#FFFFFF',
                md_bg_color='#00C853',
                font_name="Ancizar_botones",
                theme_text_color="Custom"
            )
        )

        contenedor_principal = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(16),
            adaptive_height=True
        )
        contenedor_principal.add_widget(card_contenido)
        contenedor_principal.add_widget(botones_layout)

        self.edit_dialog = MDDialog(
            title="Editar producto",
            type="custom",
            content_cls=contenedor_principal
        )
        self.edit_dialog.open()


    
    def guardar_edicion_producto(self, fecha):
        nombre = self.campos_edicion["nombre"].text.strip()
        precio = float(self.campos_edicion["precio"].text.strip())
        cantidad = int(self.campos_edicion["cantidad"].text.strip())

        nombre_antiguo, cantidad_ant, precio_ant, _ = self.producto_editado

        # Actualizar en la base de datos
        ConsultaHistorial.actualizar_producto_en_fecha(
            fecha=fecha,
            nombre_antiguo=nombre_antiguo,
            nombre_nuevo=nombre,
            precio=precio,
            cantidad=cantidad
        )

        self.edit_dialog.dismiss()
        self.mostrar_detalles(fecha)# Refresca lista y total