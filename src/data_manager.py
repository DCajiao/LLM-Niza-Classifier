import json
import os
import pandas as pd
from datetime import datetime

# Definir la ruta al archivo de datos
DATA_FILE = "emprendedores_data.csv"

def guardar_datos(datos_usuario):
    """
    Guarda los datos del usuario en un archivo CSV.
    
    Args:
        datos_usuario (dict): Diccionario con los datos del usuario
    """
    # Crear una copia de los datos para evitar modificar el original
    datos = datos_usuario.copy()
    
    # Convertir el diccionario de clasificaciones a formato JSON para almacenar
    if datos.get('clasificaciones_niza'):
        datos['clasificaciones_niza'] = json.dumps(datos['clasificaciones_niza'])
    
    # Crear DataFrame con los datos
    df_nuevo = pd.DataFrame([datos])
    
    # Verificar si el archivo ya existe
    if os.path.exists(DATA_FILE):
        # Cargar datos existentes
        df_existente = pd.read_csv(DATA_FILE)
        
        # Concatenar con nuevos datos
        df_combinado = pd.concat([df_existente, df_nuevo], ignore_index=True)
        
        # Guardar datos combinados
        df_combinado.to_csv(DATA_FILE, index=False)
    else:
        # Crear nuevo archivo con los datos
        df_nuevo.to_csv(DATA_FILE, index=False)

def cargar_datos():
    """
    Carga los datos de los emprendedores desde el archivo CSV.
    
    Returns:
        pandas.DataFrame: DataFrame con los datos de los emprendedores
    """
    if not os.path.exists(DATA_FILE):
        # Si el archivo no existe, devolver un DataFrame vacío
        return pd.DataFrame()
    
    try:
        # Cargar datos del archivo CSV
        df = pd.read_csv(DATA_FILE)
        
        # Convertir las columnas de clasificaciones de JSON a diccionarios para procesamiento
        if 'clasificaciones_niza' in df.columns:
            df['clasificaciones_niza'] = df['clasificaciones_niza'].apply(
                lambda x: json.loads(x) if isinstance(x, str) and x.strip() else None
            )
        
        return df
    
    except Exception as e:
        print(f"Error al cargar datos: {str(e)}")
        return pd.DataFrame()

def obtener_estadisticas():
    """
    Genera estadísticas de los datos de emprendedores.
    
    Returns:
        dict: Diccionario con estadísticas calculadas
    """
    df = cargar_datos()
    
    if df.empty:
        return {
            "total_emprendedores": 0,
            "promedio_edad": 0,
            "universidades": [],
            "carreras": []
        }
    
    # Calcular estadísticas básicas
    estadisticas = {
        "total_emprendedores": len(df),
        "promedio_edad": df['edad'].astype(float).mean() if 'edad' in df.columns else 0,
        "universidades": df['universidad'].value_counts().to_dict() if 'universidad' in df.columns else {},
        "carreras": df['carrera'].value_counts().to_dict() if 'carrera' in df.columns else {},
        "experiencia_previa": df['experiencia_previa'].value_counts().to_dict() if 'experiencia_previa' in df.columns else {}
    }
    
    return estadisticas
