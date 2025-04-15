import os
import datetime
from flask import render_template
from weasyprint import HTML, CSS
from io import BytesIO

def generate_pdf(data):
    """
    Genera un archivo PDF basado en los datos proporcionados utilizando una plantilla HTML.
    
    Args:
        data (dict): Diccionario con los datos para incluir en el PDF
    
    Returns:
        BytesIO: Objeto con el contenido del PDF en memoria
    """
    # Añadir fecha de generación y año actuales
    current_date = datetime.datetime.now()
    data['fecha_generacion'] = current_date.strftime('%d/%m/%Y %H:%M')
    data['year'] = current_date.year
    
    # Renderizar la plantilla con los datos
    rendered_template = render_template('pdf_template.html', data=data)
    
    # Crear el PDF a partir del HTML renderizado
    html = HTML(string=rendered_template)
    
    # Generar el PDF en un buffer en memoria
    pdf_buffer = BytesIO()
    html.write_pdf(pdf_buffer)
    
    # Resetear el puntero del buffer para poder leerlo
    pdf_buffer.seek(0)
    
    return pdf_buffer

def get_sample_data():
    """
    Genera datos de ejemplo para probar la generación de PDF.
    Útil para pruebas o demostración.
    
    Returns:
        dict: Datos de ejemplo
    """
    return {
        'nombre': 'Juan Pérez García',
        'email': 'juan.perez@universidad.edu',
        'edad': 22,
        'universidad': 'Universidad Nacional Autónoma',
        'carrera': 'Ingeniería en Sistemas Computacionales',
        'semestre': '7mo Semestre',
        'nombre_emprendimiento': 'TechSolutions MX',
        'fecha_creacion': '15/03/2024',
        'descripcion': 'TechSolutions MX es una empresa de desarrollo de software especializada en crear soluciones tecnológicas para pequeñas y medianas empresas. Ofrecemos servicios de desarrollo de aplicaciones web y móviles, consultoría en transformación digital y soporte técnico. Nuestro enfoque es proporcionar herramientas digitales accesibles y personalizadas que ayuden a las PyMEs a optimizar sus procesos y aumentar su competitividad en el mercado digital.',
        'clasificaciones': {
            'Clase 9': {
                'titulo': 'Aparatos e instrumentos científicos',
                'descripcion': 'Software, aplicaciones descargables, programas informáticos, hardware.',
                'relevancia': 95
            },
            'Clase 42': {
                'titulo': 'Servicios científicos y tecnológicos',
                'descripcion': 'Diseño y desarrollo de software, consultoría tecnológica, servicios informáticos.',
                'relevancia': 90
            },
            'Clase 35': {
                'titulo': 'Publicidad y negocios',
                'descripcion': 'Consultoría empresarial, servicios de gestión comercial, marketing digital.',
                'relevancia': 75
            }
        }
    }