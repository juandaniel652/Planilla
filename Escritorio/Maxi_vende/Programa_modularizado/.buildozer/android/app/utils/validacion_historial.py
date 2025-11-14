from kivymd.toast import toast  # O usa Snackbar si lo prefieres

def validar_campos_producto_edicion(nombre, precio, cantidad):
    """
    Valida los campos de edición del producto.
    Retorna True si son válidos, o False si hay error y muestra un mensaje.
    """
    if not nombre.strip():
        toast("El nombre no puede estar vacío")
        return False

    try:
        precio_f = float(precio)
        if precio_f <= 0:
            toast("El precio debe ser mayor que 0")
            return False
    except ValueError:
        toast("El precio debe ser un número válido")
        return False

    try:
        cantidad_i = int(cantidad)
        if cantidad_i <= 0:
            toast("La cantidad debe ser un entero mayor que 0")
            return False
    except ValueError:
        toast("La cantidad debe ser un número entero válido")
        return False

    return True
