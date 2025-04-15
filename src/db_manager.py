import os
import json
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, MetaData, Table
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv()

# Obtener la URL de conexión a la base de datos desde las variables de entorno
DATABASE_URL = os.environ.get("DATABASE_URL")

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Definir la tabla de emprendedores
metadata = MetaData()
emprendedores = Table(
    'emprendedores', 
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(255), nullable=False),
    Column('email', String(255)),
    Column('edad', Integer),
    Column('universidad', String(255)),
    Column('carrera', String(255)),
    Column('semestre', String(50)),
    Column('experiencia_previa', String(10)),
    Column('nombre_emprendimiento', String(255)),
    Column('descripcion_emprendimiento', Text),
    Column('clasificaciones_niza', JSONB),
    Column('fecha_registro', DateTime, default=datetime.now)
)

def guardar_datos_db(datos_usuario):
    """
    Guarda los datos del usuario en la base de datos.
    
    Args:
        datos_usuario (dict): Diccionario con los datos del usuario
    """
    try:
        # Crear una copia de los datos para evitar modificar el original
        datos = datos_usuario.copy()
        
        # Convertir la edad a entero si es un string
        if 'edad' in datos and datos['edad']:
            try:
                datos['edad'] = int(datos['edad'])
            except (ValueError, TypeError):
                datos['edad'] = None
        
        # Convertir el diccionario de clasificaciones a formato JSON para almacenar
        if datos.get('clasificaciones_niza'):
            if isinstance(datos['clasificaciones_niza'], dict):
                datos['clasificaciones_niza'] = datos['clasificaciones_niza']
            elif isinstance(datos['clasificaciones_niza'], str):
                datos['clasificaciones_niza'] = json.loads(datos['clasificaciones_niza'])
        
        # Crear conexión a la base de datos
        with engine.connect() as connection:
            # Insertar datos en la tabla
            connection.execute(emprendedores.insert().values(**datos))
            connection.commit()
        
        return True
    
    except Exception as e:
        print(f"Error al guardar datos en la base de datos: {str(e)}")
        return False

def cargar_datos_db():
    """
    Carga los datos de los emprendedores desde la base de datos.
    
    Returns:
        pandas.DataFrame: DataFrame con los datos de los emprendedores
    """
    try:
        # Crear conexión a la base de datos
        with engine.connect() as connection:
            # Consultar todos los datos de la tabla
            result = connection.execute(emprendedores.select())
            
            # Convertir el resultado a un DataFrame de pandas
            df = pd.DataFrame(result.fetchall())
            
            # Si no hay datos, devolver un DataFrame vacío
            if df.empty:
                return pd.DataFrame()
            
            # Establecer los nombres de las columnas
            df.columns = result.keys()
            
            return df
    
    except Exception as e:
        print(f"Error al cargar datos de la base de datos: {str(e)}")
        return pd.DataFrame()

def obtener_estadisticas_db():
    """
    Genera estadísticas de los datos de emprendedores desde la base de datos.
    
    Returns:
        dict: Diccionario con estadísticas calculadas
    """
    df = cargar_datos_db()
    
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