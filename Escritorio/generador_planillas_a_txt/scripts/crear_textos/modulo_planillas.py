# crear_textos/modulo_planillas.py
from backend.db_utils import insertar_planilla

def guardar_planilla_en_db(planilla: dict):
    """
    Guarda un diccionario de planilla en la tabla 'planillas' de Supabase.
    """
    tabla = "planillas"  # Cambiar si tu tabla tiene otro nombre
    insertar_planilla(tabla, planilla)
    print(f"Planilla '{planilla.get('nombre')}' guardada en la DB.")
