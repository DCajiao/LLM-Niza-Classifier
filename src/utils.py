import re

def validar_datos(datos, campos_requeridos):
    """
    Valida que todos los campos requeridos estén presentes y no estén vacíos.
    
    Args:
        datos (dict): Diccionario con los datos a validar
        campos_requeridos (list): Lista de nombres de campos que deben estar presentes
        
    Returns:
        bool: True si todos los campos requeridos están presentes y no vacíos, False en caso contrario
    """
    for campo in campos_requeridos:
        if campo not in datos or not datos[campo]:
            return False
    return True

def validar_email(email):
    """
    Valida que una dirección de correo electrónico tenga un formato válido.
    
    Args:
        email (str): Dirección de correo electrónico a validar
        
    Returns:
        bool: True si la dirección tiene un formato válido, False en caso contrario
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validar_numero(numero, min_valor=None, max_valor=None):
    """
    Valida que un valor sea un número dentro de un rango especificado.
    
    Args:
        numero (str): Valor a validar
        min_valor (int, optional): Valor mínimo permitido
        max_valor (int, optional): Valor máximo permitido
        
    Returns:
        bool: True si el valor es un número válido dentro del rango, False en caso contrario
    """
    try:
        num = float(numero)
        
        if min_valor is not None and num < min_valor:
            return False
        
        if max_valor is not None and num > max_valor:
            return False
        
        return True
    
    except (ValueError, TypeError):
        return False

def limpiar_texto(texto):
    """
    Limpia un texto eliminando caracteres especiales y espacios en blanco extras.
    
    Args:
        texto (str): Texto a limpiar
        
    Returns:
        str: Texto limpio
    """
    if not texto:
        return ""
    
    # Eliminar espacios en blanco extras
    texto = re.sub(r'\s+', ' ', texto.strip())
    
    return texto

def formatear_nombre(nombre):
    """
    Formatea un nombre propio capitalizando cada palabra.
    
    Args:
        nombre (str): Nombre a formatear
        
    Returns:
        str: Nombre formateado
    """
    if not nombre:
        return ""
    
    palabras = nombre.split()
    palabras_formateadas = [palabra.capitalize() for palabra in palabras]
    
    return " ".join(palabras_formateadas)
