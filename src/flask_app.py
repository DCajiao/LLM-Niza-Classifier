from flask import Flask, render_template_string, request, jsonify, session, make_response, render_template, send_file, redirect
import os
import json
import datetime
from pdf_generator import generate_pdf, get_sample_data
from werkzeug.utils import secure_filename
from llm_huggingface import obtener_clasificaciones_niza_hf

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key para las sesiones

# Configuración de la app
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['WTF_CSRF_ENABLED'] = False  # Desactivar CSRF para simplificar la demo

@app.route('/')
def index():
    return redirect('/paso1')

@app.route('/paso1', methods=['GET'])
def paso1():
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clasificador de Emprendimientos - Niza</title>
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #111827;
                background-color: #F9FAFB;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #4F46E5;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .step-indicators {
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
            }
            .step {
                text-align: center;
                flex: 1;
                position: relative;
            }
            .step-circle {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #E5E7EB;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 10px;
                font-weight: bold;
                color: #6B7280;
            }
            .step.active .step-circle {
                background-color: #4F46E5;
                color: white;
            }
            .step.completed .step-circle {
                background-color: #10B981;
                color: white;
            }
            .step-label {
                font-size: 14px;
                color: #6B7280;
            }
            .step.active .step-label {
                color: #4F46E5;
                font-weight: bold;
            }
            .step.completed .step-label {
                color: #10B981;
                font-weight: bold;
            }
            .card {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
            }
            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                font-size: 16px;
            }
            button {
                background-color: #4F46E5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                margin: 0 5px;
            }
            button:hover {
                background-color: #4338CA;
                transform: translateY(-2px);
            }
            .btn-back {
                background-color: #F3F4F6;
                color: #4B5563;
                border: 1px solid #D1D5DB;
            }
            .btn-back:hover {
                background-color: #E5E7EB;
            }
            .btn-download {
                background-color: #047857;
            }
            .btn-download:hover {
                background-color: #065F46;
            }
            .navigation {
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            }
            .success-message {
                background-color: #D1FAE5;
                border-left: 4px solid #10B981;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Clasificador de Emprendimientos Universitarios - Niza</h1>
        </div>
        
        <div class="step-indicators">
            <div class="step active">
                <div class="step-circle">1</div>
                <div class="step-label">Datos personales</div>
            </div>
            <div class="step">
                <div class="step-circle">2</div>
                <div class="step-label">Información académica</div>
            </div>
            <div class="step">
                <div class="step-circle">3</div>
                <div class="step-label">Emprendimiento</div>
            </div>
            <div class="step">
                <div class="step-circle">4</div>
                <div class="step-label">Clasificación</div>
            </div>
            <div class="step">
                <div class="step-circle">5</div>
                <div class="step-label">Resultado</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Paso 1: Información Personal</h2>
            <p>Para comenzar, por favor comparte tus datos personales básicos.</p>
            
            <form id="paso1Form" method="post" action="/enviar_paso1">
                <div class="form-group">
                    <label for="nombre">Nombre Completo *</label>
                    <input type="text" id="nombre" name="nombre" placeholder="Ej. Juan Pérez García" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Correo Electrónico *</label>
                    <input type="email" id="email" name="email" placeholder="tu.email@universidad.edu" required>
                </div>
                
                <div class="form-group">
                    <label for="edad">Edad *</label>
                    <input type="number" id="edad" name="edad" min="16" max="80" value="18" required>
                </div>
                
                <div class="form-group">
                    <label for="universidad">Universidad *</label>
                    <input type="text" id="universidad" name="universidad" placeholder="Nombre de tu universidad" required>
                </div>
                
                <div class="navigation">
                    <div></div> <!-- Espacio vacío para alineación -->
                    <button type="submit">Continuar →</button>
                </div>
            </form>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <p>Esta aplicación te ayuda a clasificar tu emprendimiento según las categorías Niza para registro de marcas.</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)

@app.route('/enviar_paso1', methods=['POST'])
def enviar_paso1():
    # Guardar datos del paso 1 en la sesión
    session['paso1_data'] = {
        'nombre': request.form.get('nombre', ''),
        'email': request.form.get('email', ''),
        'edad': request.form.get('edad', ''),
        'universidad': request.form.get('universidad', '')
    }
    return redirect('/paso2')

@app.route('/paso2', methods=['GET'])
def paso2():
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clasificador de Emprendimientos - Niza</title>
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #111827;
                background-color: #F9FAFB;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #4F46E5;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .step-indicators {
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
            }
            .step {
                text-align: center;
                flex: 1;
                position: relative;
            }
            .step-circle {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #E5E7EB;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 10px;
                font-weight: bold;
                color: #6B7280;
            }
            .step.active .step-circle {
                background-color: #4F46E5;
                color: white;
            }
            .step.completed .step-circle {
                background-color: #10B981;
                color: white;
            }
            .step-label {
                font-size: 14px;
                color: #6B7280;
            }
            .step.active .step-label {
                color: #4F46E5;
                font-weight: bold;
            }
            .step.completed .step-label {
                color: #10B981;
                font-weight: bold;
            }
            .card {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
            }
            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                font-size: 16px;
            }
            button {
                background-color: #4F46E5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                margin: 0 5px;
            }
            button:hover {
                background-color: #4338CA;
                transform: translateY(-2px);
            }
            .btn-back {
                background-color: #F3F4F6;
                color: #4B5563;
                border: 1px solid #D1D5DB;
            }
            .btn-back:hover {
                background-color: #E5E7EB;
            }
            .navigation {
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Clasificador de Emprendimientos Universitarios - Niza</h1>
        </div>
        
        <div class="step-indicators">
            <div class="step completed">
                <div class="step-circle">1</div>
                <div class="step-label">Datos personales</div>
            </div>
            <div class="step active">
                <div class="step-circle">2</div>
                <div class="step-label">Información académica</div>
            </div>
            <div class="step">
                <div class="step-circle">3</div>
                <div class="step-label">Emprendimiento</div>
            </div>
            <div class="step">
                <div class="step-circle">4</div>
                <div class="step-label">Clasificación</div>
            </div>
            <div class="step">
                <div class="step-circle">5</div>
                <div class="step-label">Resultado</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Paso 2: Información Académica</h2>
            <p>Ahora, cuéntanos un poco sobre tu trayectoria académica.</p>
            
            <form id="paso2Form" method="post" action="/enviar_paso2">
                <div class="form-group">
                    <label for="carrera">Carrera/Programa *</label>
                    <input type="text" id="carrera" name="carrera" placeholder="Ej. Ingeniería en Sistemas, Administración de Empresas" required>
                </div>
                
                <div class="form-group">
                    <label for="semestre">Semestre/Año que cursas *</label>
                    <select id="semestre" name="semestre" required>
                        <option value="">Selecciona una opción</option>
                        <option value="1er Semestre">1er Semestre</option>
                        <option value="2do Semestre">2do Semestre</option>
                        <option value="3er Semestre">3er Semestre</option>
                        <option value="4to Semestre">4to Semestre</option>
                        <option value="5to Semestre">5to Semestre</option>
                        <option value="6to Semestre">6to Semestre</option>
                        <option value="7mo Semestre">7mo Semestre</option>
                        <option value="8vo Semestre">8vo Semestre</option>
                        <option value="9no Semestre">9no Semestre</option>
                        <option value="10mo Semestre">10mo Semestre</option>
                        <option value="Maestría">Maestría</option>
                        <option value="Doctorado">Doctorado</option>
                        <option value="Egresado">Egresado</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="intereses">Áreas de interés académico/profesional</label>
                    <textarea id="intereses" name="intereses" rows="3" placeholder="Ej. Desarrollo de software, Marketing digital, Finanzas"></textarea>
                </div>
                
                <div class="navigation">
                    <a href="/paso1" class="btn-back">← Anterior</a>
                    <button type="submit">Continuar →</button>
                </div>
            </form>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <p>Esta información nos ayudará a entender mejor tu perfil académico y emprendedor.</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)

@app.route('/enviar_paso2', methods=['POST'])
def enviar_paso2():
    # Guardar datos del paso 2 en la sesión
    session['paso2_data'] = {
        'carrera': request.form.get('carrera', ''),
        'semestre': request.form.get('semestre', ''),
        'intereses': request.form.get('intereses', '')
    }
    return redirect('/paso3')

@app.route('/paso3', methods=['GET'])
def paso3():
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clasificador de Emprendimientos - Niza</title>
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #111827;
                background-color: #F9FAFB;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #4F46E5;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .step-indicators {
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
            }
            .step {
                text-align: center;
                flex: 1;
                position: relative;
            }
            .step-circle {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #E5E7EB;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 10px;
                font-weight: bold;
                color: #6B7280;
            }
            .step.active .step-circle {
                background-color: #4F46E5;
                color: white;
            }
            .step.completed .step-circle {
                background-color: #10B981;
                color: white;
            }
            .step-label {
                font-size: 14px;
                color: #6B7280;
            }
            .step.active .step-label {
                color: #4F46E5;
                font-weight: bold;
            }
            .step.completed .step-label {
                color: #10B981;
                font-weight: bold;
            }
            .card {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
            }
            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                font-size: 16px;
            }
            button {
                background-color: #4F46E5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                margin: 0 5px;
            }
            button:hover {
                background-color: #4338CA;
                transform: translateY(-2px);
            }
            .btn-back {
                background-color: #F3F4F6;
                color: #4B5563;
                border: 1px solid #D1D5DB;
            }
            .btn-back:hover {
                background-color: #E5E7EB;
            }
            .navigation {
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Clasificador de Emprendimientos Universitarios - Niza</h1>
        </div>
        
        <div class="step-indicators">
            <div class="step completed">
                <div class="step-circle">1</div>
                <div class="step-label">Datos personales</div>
            </div>
            <div class="step completed">
                <div class="step-circle">2</div>
                <div class="step-label">Información académica</div>
            </div>
            <div class="step active">
                <div class="step-circle">3</div>
                <div class="step-label">Emprendimiento</div>
            </div>
            <div class="step">
                <div class="step-circle">4</div>
                <div class="step-label">Clasificación</div>
            </div>
            <div class="step">
                <div class="step-circle">5</div>
                <div class="step-label">Resultado</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Paso 3: Información del Emprendimiento</h2>
            <p>Ahora, háblanos sobre tu proyecto o emprendimiento.</p>
            
            <form id="paso3Form" method="post" action="/enviar_paso3">
                <div class="form-group">
                    <label for="nombre_emprendimiento">Nombre del Emprendimiento *</label>
                    <input type="text" id="nombre_emprendimiento" name="nombre_emprendimiento" placeholder="Nombre de tu marca o proyecto" required>
                </div>
                
                <div class="form-group">
                    <label for="fecha_creacion">Fecha de Creación</label>
                    <input type="date" id="fecha_creacion" name="fecha_creacion">
                </div>
                
                <div class="form-group">
                    <label for="descripcion">Descripción detallada del emprendimiento *</label>
                    <textarea id="descripcion" name="descripcion" rows="5" placeholder="Describe tu proyecto, los productos o servicios que ofreces, el público al que va dirigido y cualquier otra información relevante..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="sector">Sector principal</label>
                    <select id="sector" name="sector">
                        <option value="">Selecciona un sector (opcional)</option>
                        <option value="Tecnología">Tecnología</option>
                        <option value="Salud">Salud</option>
                        <option value="Educación">Educación</option>
                        <option value="Finanzas">Finanzas</option>
                        <option value="Alimentación">Alimentación</option>
                        <option value="Moda">Moda</option>
                        <option value="Arte y cultura">Arte y cultura</option>
                        <option value="Deporte">Deporte</option>
                        <option value="Turismo">Turismo</option>
                        <option value="Sostenibilidad">Sostenibilidad</option>
                        <option value="Otro">Otro</option>
                    </select>
                </div>
                
                <div class="navigation">
                    <a href="/paso2" class="btn-back">← Anterior</a>
                    <button type="submit">Continuar →</button>
                </div>
            </form>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <p>La descripción detallada de tu emprendimiento es clave para determinar las clasificaciones Niza más adecuadas.</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)

@app.route('/enviar_paso3', methods=['POST'])
def enviar_paso3():
    # Guardar datos del paso 3 en la sesión
    nombre_emprendimiento = request.form.get('nombre_emprendimiento', '')
    descripcion = request.form.get('descripcion', '')
    sector = request.form.get('sector', '')
    
    session['paso3_data'] = {
        'nombre_emprendimiento': nombre_emprendimiento,
        'fecha_creacion': request.form.get('fecha_creacion', ''),
        'descripcion': descripcion,
        'sector': sector
    }
    
    # Analizar la descripción para generar clasificaciones Niza relevantes
    # Primero, intentar usar Hugging Face LLM para un análisis avanzado
    try:
        # Crear un prompt combinado con la descripción y el sector
        descripcion_completa = f"Descripción del emprendimiento: {descripcion}\nSector principal: {sector}"
        # Llamar a la función de Hugging Face para análisis con LLM
        resultado_hf = obtener_clasificaciones_niza_hf(descripcion_completa)
        
        # Si la respuesta contiene un error o no hay clasificaciones, usar el método fallback
        if "Error" in str(resultado_hf) or not resultado_hf.get("clasificaciones"):
            print("Usando método fallback para clasificación Niza debido a error en HF API")
            clases_niza = obtener_clasificaciones_basadas_en_descripcion(descripcion, sector)
        else:
            # Convertir el formato de HF al formato esperado por la aplicación
            clases_niza = {}
            for clasificacion in resultado_hf.get("clasificaciones", []):
                numero_clase = clasificacion.get("clase", "")
                if numero_clase.isdigit():
                    clase_key = f"Clase {numero_clase}"
                    clases_niza[clase_key] = {
                        'titulo': clasificacion.get("descripcion", "")[:50] + "...",
                        'descripcion': clasificacion.get("descripcion", ""),
                        'relevancia': clasificacion.get("confianza", 50)
                    }
    except Exception as e:
        print(f"Error al procesar con HF: {str(e)}")
        # En caso de error, usar el método fallback
        clases_niza = obtener_clasificaciones_basadas_en_descripcion(descripcion, sector)
    
    session['clasificaciones_niza'] = clases_niza
    
    return redirect('/paso4')

def obtener_clasificaciones_basadas_en_descripcion(descripcion, sector):
    """
    Analiza la descripción del emprendimiento para determinar las clasificaciones Niza más apropiadas.
    En una implementación real, este análisis se haría con un modelo de IA.
    
    Args:
        descripcion (str): Descripción del emprendimiento
        sector (str): Sector principal del emprendimiento
    
    Returns:
        dict: Clasificaciones Niza relevantes para la descripción
    """
    descripcion = descripcion.lower()
    sector = sector.lower()
    
    # Diccionario de palabras clave para diferentes tipos de negocios
    palabras_clave = {
        'tecnologia': ['software', 'aplicación', 'app', 'tecnología', 'digital', 'web', 'internet', 'computadora', 'móvil', 'programación'],
        'alimentos_bebidas': ['alimento', 'comida', 'bebida', 'restaurante', 'café', 'cerveza', 'vino', 'cocina', 'gastronomía', 'pastelería', 'panadería'],
        'moda': ['ropa', 'moda', 'vestido', 'textil', 'calzado', 'diseño', 'accesorios', 'joyería', 'bolsos'],
        'salud': ['salud', 'médico', 'clínica', 'bienestar', 'terapia', 'farmacia', 'medicina', 'nutrición'],
        'educacion': ['educación', 'enseñanza', 'curso', 'formación', 'academia', 'escuela', 'aprendizaje', 'capacitación'],
        'arte_cultura': ['arte', 'pintura', 'música', 'danza', 'teatro', 'cultura', 'cine', 'diseño', 'fotografía']
    }
    
    # Contar coincidencias para cada categoría
    coincidencias = {categoria: 0 for categoria in palabras_clave}
    
    for categoria, palabras in palabras_clave.items():
        for palabra in palabras:
            if palabra in descripcion:
                coincidencias[categoria] += 1
    
    # Si sector está definido, aumentar su relevancia
    for categoria in coincidencias:
        for palabra in palabras_clave[categoria]:
            if palabra in sector:
                coincidencias[categoria] += 3  # Dar más peso al sector declarado
    
    # Determinar categoría principal
    categoria_principal = 'general'
    max_coincidencias = 0
    
    for categoria, valor in coincidencias.items():
        if valor > max_coincidencias:
            max_coincidencias = valor
            categoria_principal = categoria
    
    # Si todas las categorías tienen 0 coincidencias, mantener 'general'
    
    # Asignar clasificaciones Niza basadas en la categoría
    clasificaciones = {}
    
    if categoria_principal == 'tecnologia':
        clasificaciones = {
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
                'relevancia': 70
            }
        }
    elif categoria_principal == 'alimentos_bebidas':
        clasificaciones = {
            'Clase 30': {
                'titulo': 'Café, té, cacao y sucedáneos',
                'descripcion': 'Alimentos de origen vegetal preparados para consumir, productos de pastelería, confitería.',
                'relevancia': 90
            },
            'Clase 32': {
                'titulo': 'Cervezas y bebidas sin alcohol',
                'descripcion': 'Cervezas, aguas minerales, bebidas a base de frutas, preparaciones para elaborar bebidas.',
                'relevancia': 95
            },
            'Clase 43': {
                'titulo': 'Servicios de restauración',
                'descripcion': 'Servicios de restaurante, bar, cafetería, servicios de catering.',
                'relevancia': 85
            }
        }
    elif categoria_principal == 'moda':
        clasificaciones = {
            'Clase 25': {
                'titulo': 'Prendas de vestir, calzado',
                'descripcion': 'Ropa, calzado, sombreros, prendas de vestir, artículos de sombrerería.',
                'relevancia': 95
            },
            'Clase 18': {
                'titulo': 'Cuero e imitaciones de cuero',
                'descripcion': 'Bolsos, maletas, carteras, mochilas, artículos de marroquinería.',
                'relevancia': 85
            },
            'Clase 35': {
                'titulo': 'Publicidad y negocios',
                'descripcion': 'Servicios de venta minorista, publicidad, gestión comercial.',
                'relevancia': 75
            }
        }
    elif categoria_principal == 'salud':
        clasificaciones = {
            'Clase 5': {
                'titulo': 'Productos farmacéuticos',
                'descripcion': 'Preparaciones médicas, complementos alimenticios, productos higiénicos.',
                'relevancia': 95
            },
            'Clase 44': {
                'titulo': 'Servicios médicos',
                'descripcion': 'Servicios médicos, terapéuticos, de asistencia sanitaria.',
                'relevancia': 90
            },
            'Clase 10': {
                'titulo': 'Aparatos e instrumentos quirúrgicos',
                'descripcion': 'Aparatos médicos, ortopédicos, artículos para terapias médicas.',
                'relevancia': 75
            }
        }
    elif categoria_principal == 'educacion':
        clasificaciones = {
            'Clase 41': {
                'titulo': 'Educación y formación',
                'descripcion': 'Servicios educativos, formación, actividades culturales, cursos académicos.',
                'relevancia': 95
            },
            'Clase 16': {
                'titulo': 'Material de instrucción',
                'descripcion': 'Publicaciones impresas, libros, material didáctico, textos educativos.',
                'relevancia': 75
            },
            'Clase 35': {
                'titulo': 'Publicidad y negocios',
                'descripcion': 'Servicios de gestión administrativa, organización de actividades comerciales.',
                'relevancia': 60
            }
        }
    elif categoria_principal == 'arte_cultura':
        clasificaciones = {
            'Clase 41': {
                'titulo': 'Educación y formación',
                'descripcion': 'Actividades culturales y artísticas, entretenimiento, organización de exposiciones.',
                'relevancia': 90
            },
            'Clase 16': {
                'titulo': 'Material impreso',
                'descripcion': 'Obras de arte, productos de imprenta, fotografías, pinturas.',
                'relevancia': 85
            },
            'Clase 35': {
                'titulo': 'Publicidad y negocios',
                'descripcion': 'Servicios de galería de arte, comercialización de obras artísticas.',
                'relevancia': 70
            }
        }
    else:  # Categoría general
        clasificaciones = {
            'Clase 35': {
                'titulo': 'Publicidad y negocios',
                'descripcion': 'Servicios de gestión comercial, publicidad, marketing, administración de negocios.',
                'relevancia': 90
            },
            'Clase 41': {
                'titulo': 'Educación y formación',
                'descripcion': 'Servicios de formación, actividades culturales, organización de eventos.',
                'relevancia': 75
            },
            'Clase 42': {
                'titulo': 'Servicios científicos y tecnológicos',
                'descripcion': 'Servicios de investigación, desarrollo de productos, diseño de artículos.',
                'relevancia': 65
            }
        }
    
    # Si "cerveza" está en la descripción, asegurar clase 32
    if "cerveza" in descripcion or "cervecería" in descripcion or ("artesanal" in descripcion and "bebida" in descripcion):
        clasificaciones['Clase 32'] = {
            'titulo': 'Cervezas y bebidas sin alcohol',
            'descripcion': 'Cervezas, cervezas artesanales, bebidas a base de malta, preparaciones para elaborar cervezas.',
            'relevancia': 95
        }
        
        # Añadir también clase 40 para servicios de elaboración de cerveza
        clasificaciones['Clase 40'] = {
            'titulo': 'Tratamiento de materiales',
            'descripcion': 'Servicios de elaboración de cervezas, destilación, elaboración de bebidas.',
            'relevancia': 85
        }
        
        # Si tiene un espacio físico, añadir clase 43
        if "bar" in descripcion or "restaurante" in descripcion or "taproom" in descripcion:
            clasificaciones['Clase 43'] = {
                'titulo': 'Servicios de restauración',
                'descripcion': 'Servicios de bar, cervecería, restaurante, taproom, degustación de cerveza.',
                'relevancia': 90
            }
    
    return clasificaciones

@app.route('/paso4', methods=['GET'])
def paso4():
    # Obtener las clasificaciones generadas en el paso anterior
    clasificaciones_niza = session.get('clasificaciones_niza', {})
    
    # Generar HTML para mostrar las clasificaciones
    clasificaciones_html = ""
    for clase, datos in clasificaciones_niza.items():
        titulo = datos.get('titulo', '')
        descripcion = datos.get('descripcion', '')
        relevancia = datos.get('relevancia', 0)
        
        clasificaciones_html += f'''
        <div class="class-item">
            <div class="class-title">{clase}: {titulo}</div>
            <div class="class-description">{descripcion}</div>
            <div class="class-checkbox">
                <input type="checkbox" id="{clase.replace(' ', '_')}" name="clases_seleccionadas" value="{clase}" checked>
                <label for="{clase.replace(' ', '_')}">Seleccionar esta clase ({relevancia}% de relevancia)</label>
            </div>
        </div>
        '''
    
    # Si no hay clasificaciones, mostrar mensaje
    if not clasificaciones_html:
        clasificaciones_html = '''
        <div class="info-box" style="background-color: #FEF2F2; border-left: 4px solid #EF4444;">
            <p>No se han podido generar clasificaciones para tu emprendimiento. Por favor, regresa al paso anterior y proporciona una descripción más detallada.</p>
        </div>
        '''
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clasificador de Emprendimientos - Niza</title>
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #111827;
                background-color: #F9FAFB;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #4F46E5;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .step-indicators {
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
            }
            .step {
                text-align: center;
                flex: 1;
                position: relative;
            }
            .step-circle {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #E5E7EB;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 10px;
                font-weight: bold;
                color: #6B7280;
            }
            .step.active .step-circle {
                background-color: #4F46E5;
                color: white;
            }
            .step.completed .step-circle {
                background-color: #10B981;
                color: white;
            }
            .step-label {
                font-size: 14px;
                color: #6B7280;
            }
            .step.active .step-label {
                color: #4F46E5;
                font-weight: bold;
            }
            .step.completed .step-label {
                color: #10B981;
                font-weight: bold;
            }
            .card {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
            }
            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                font-size: 16px;
            }
            button {
                background-color: #4F46E5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                margin: 0 5px;
            }
            button:hover {
                background-color: #4338CA;
                transform: translateY(-2px);
            }
            .btn-back {
                background-color: #F3F4F6;
                color: #4B5563;
                border: 1px solid #D1D5DB;
            }
            .btn-back:hover {
                background-color: #E5E7EB;
            }
            .navigation {
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            }
            .class-item {
                background-color: #F9FAFB;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                border-left: 4px solid #4F46E5;
            }
            .class-title {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .class-description {
                font-size: 14px;
                color: #4B5563;
                margin-bottom: 10px;
            }
            .class-checkbox {
                display: flex;
                align-items: center;
                margin-top: 10px;
            }
            .class-checkbox input {
                width: auto;
                margin-right: 10px;
            }
            .info-box {
                background-color: #EFF6FF;
                border-left: 4px solid #3B82F6;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .loading {
                text-align: center;
                padding: 40px 0;
            }
            .loading-spinner {
                border: 5px solid #f3f3f3;
                border-top: 5px solid #4F46E5;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Clasificador de Emprendimientos Universitarios - Niza</h1>
        </div>
        
        <div class="step-indicators">
            <div class="step completed">
                <div class="step-circle">1</div>
                <div class="step-label">Datos personales</div>
            </div>
            <div class="step completed">
                <div class="step-circle">2</div>
                <div class="step-label">Información académica</div>
            </div>
            <div class="step completed">
                <div class="step-circle">3</div>
                <div class="step-label">Emprendimiento</div>
            </div>
            <div class="step active">
                <div class="step-circle">4</div>
                <div class="step-label">Clasificación</div>
            </div>
            <div class="step">
                <div class="step-circle">5</div>
                <div class="step-label">Resultado</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Paso 4: Clasificaciones Niza Sugeridas</h2>
            <p>Basado en la descripción de tu emprendimiento, hemos identificado las siguientes clasificaciones Niza como las más relevantes:</p>
            
            <div class="info-box">
                <p>Selecciona las clasificaciones que consideres más adecuadas para tu emprendimiento. Puedes seleccionar varias.</p>
            </div>
            
            <form id="paso4Form" method="post" action="/enviar_paso4">
                ''' + clasificaciones_html + '''
                
                <div class="form-group">
                    <label for="comentarios">Comentarios adicionales (opcional)</label>
                    <textarea id="comentarios" name="comentarios" rows="3" placeholder="¿Hay algo más que quieras comentarnos sobre tu emprendimiento o las clasificaciones sugeridas?"></textarea>
                </div>
                
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="acepto_datos" required>
                        Acepto el tratamiento de mis datos personales con fines estadísticos y de investigación, conforme a la política de privacidad.
                    </label>
                </div>
                
                <div class="navigation">
                    <a href="/paso3" class="btn-back">← Anterior</a>
                    <button type="submit">Ver resultados finales →</button>
                </div>
            </form>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <p>Las clasificaciones Niza te ayudarán a proteger tu marca en los sectores y categorías de productos/servicios relevantes para tu emprendimiento.</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)

@app.route('/enviar_paso4', methods=['POST'])
def enviar_paso4():
    # Guardar datos del paso 4 en la sesión
    session['paso4_data'] = {
        'clases_seleccionadas': request.form.getlist('clases_seleccionadas'),
        'comentarios': request.form.get('comentarios', '')
    }
    return redirect('/paso5')

@app.route('/paso5', methods=['GET'])
def paso5():
    # Obtener datos de la sesión
    paso1_data = session.get('paso1_data', {})
    paso3_data = session.get('paso3_data', {})
    clasificaciones_niza = session.get('clasificaciones_niza', {})
    
    # Nombre del emprendimiento ingresado o valor por defecto
    nombre_emprendimiento = paso3_data.get('nombre_emprendimiento', 'TechSolutions MX')
    
    # Utilizar el nombre del usuario
    nombre_usuario = paso1_data.get('nombre', 'Emprendedor')
    
    # Construir las clasificaciones en formato HTML
    clasificaciones_html = ""
    for clase, datos in clasificaciones_niza.items():
        clasificaciones_html += f'''
        <div class="class-item">
            <div class="class-title">{clase}: {datos.get('titulo', '')}</div>
            <div class="class-description">{datos.get('descripcion', '')}</div>
            <div class="class-relevance">Relevancia: {datos.get('relevancia', 0)}%</div>
        </div>
        '''
    
    # Si no hay clasificaciones, mostrar un mensaje
    if not clasificaciones_html:
        clasificaciones_html = '''
        <div class="info-box" style="background-color: #FEF2F2; border-left: 4px solid #EF4444;">
            <p>No se han podido generar clasificaciones para tu emprendimiento. Por favor, asegúrate de proporcionar una descripción detallada del mismo.</p>
        </div>
        '''
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clasificador de Emprendimientos - Resultados</title>
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #111827;
                background-color: #F9FAFB;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #4F46E5;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .step-indicators {
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
            }
            .step {
                text-align: center;
                flex: 1;
                position: relative;
            }
            .step-circle {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #E5E7EB;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 10px;
                font-weight: bold;
                color: #6B7280;
            }
            .step.active .step-circle {
                background-color: #4F46E5;
                color: white;
            }
            .step.completed .step-circle {
                background-color: #10B981;
                color: white;
            }
            .step-label {
                font-size: 14px;
                color: #6B7280;
            }
            .step.active .step-label {
                color: #4F46E5;
                font-weight: bold;
            }
            .step.completed .step-label {
                color: #10B981;
                font-weight: bold;
            }
            .card {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                margin-bottom: 30px;
            }
            .class-item {
                background-color: #F3F4F6;
                padding: 15px;
                margin-bottom: 15px;
                border-left: 4px solid #4F46E5;
                border-radius: 4px;
            }
            .class-title {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .class-relevance {
                margin-top: 10px;
                font-weight: 500;
            }
            .highlight {
                color: #4F46E5;
                font-weight: bold;
            }
            .btn-download {
                background-color: #047857;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-top: 20px;
                text-decoration: none;
            }
            .btn-download:hover {
                background-color: #065F46;
                transform: translateY(-2px);
            }
            .btn-download svg {
                margin-right: 8px;
            }
            .success-message {
                background-color: #D1FAE5;
                border-left: 4px solid #10B981;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .navigation {
                display: flex;
                justify-content: center;
                margin-top: 20px;
                gap: 10px;
            }
            .btn-start-over {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                text-decoration: none;
            }
            .btn-start-over:hover {
                background-color: #4B5563;
                transform: translateY(-2px);
            }
            .user-info {
                margin-top: 20px;
                padding: 15px;
                background-color: #F3F4F6;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Clasificador de Emprendimientos Universitarios - Niza</h1>
        </div>
        
        <div class="step-indicators">
            <div class="step completed">
                <div class="step-circle">1</div>
                <div class="step-label">Datos personales</div>
            </div>
            <div class="step completed">
                <div class="step-circle">2</div>
                <div class="step-label">Información académica</div>
            </div>
            <div class="step completed">
                <div class="step-circle">3</div>
                <div class="step-label">Emprendimiento</div>
            </div>
            <div class="step completed">
                <div class="step-circle">4</div>
                <div class="step-label">Clasificación</div>
            </div>
            <div class="step active">
                <div class="step-circle">5</div>
                <div class="step-label">Resultado</div>
            </div>
        </div>
        
        <div class="success-message">
            <p>¡Análisis completado con éxito! Hemos procesado la información de tu emprendimiento y determinado las clasificaciones Niza más relevantes.</p>
        </div>
        
        <div class="card">
            <h2>Resultados del Análisis</h2>
            <p>Para tu emprendimiento, recomendamos considerar las siguientes clasificaciones Niza para el registro de tu marca:</p>
            
        ''' + clasificaciones_html + '''
            
            <p><span class="highlight">Nota importante:</span> Estas clasificaciones son recomendaciones basadas en la descripción de tu emprendimiento. Se recomienda consultar con un especialista en propiedad intelectual antes de proceder con el registro de marca.</p>
            
            <div class="navigation">
                <a href="/generar_pdf" class="btn-download">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Descargar resultados en PDF
                </a>
                <a href="/" class="btn-start-over">Comenzar nuevo análisis</a>
            </div>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <p>Gracias por utilizar nuestro clasificador de emprendimientos. ¡Buena suerte con tu registro de marca!</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "message": "Aplicación funcionando correctamente"})

@app.route('/demo/resultados')
def demo_resultados():
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clasificador de Emprendimientos - Resultados</title>
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #111827;
                background-color: #F9FAFB;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #4F46E5;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .step-indicators {
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
            }
            .step {
                text-align: center;
                flex: 1;
                position: relative;
            }
            .step-circle {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #E5E7EB;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 10px;
                font-weight: bold;
                color: #6B7280;
            }
            .step.active .step-circle {
                background-color: #4F46E5;
                color: white;
            }
            .step.completed .step-circle {
                background-color: #10B981;
                color: white;
            }
            .step-label {
                font-size: 14px;
                color: #6B7280;
            }
            .step.active .step-label {
                color: #4F46E5;
                font-weight: bold;
            }
            .step.completed .step-label {
                color: #10B981;
                font-weight: bold;
            }
            .card {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                margin-bottom: 30px;
            }
            .class-item {
                background-color: #F3F4F6;
                padding: 15px;
                margin-bottom: 15px;
                border-left: 4px solid #4F46E5;
                border-radius: 4px;
            }
            .class-title {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .class-relevance {
                margin-top: 10px;
                font-weight: 500;
            }
            .highlight {
                color: #4F46E5;
                font-weight: bold;
            }
            .btn-download {
                background-color: #047857;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-top: 20px;
            }
            .btn-download:hover {
                background-color: #065F46;
                transform: translateY(-2px);
            }
            .btn-download svg {
                margin-right: 8px;
            }
            .success-message {
                background-color: #D1FAE5;
                border-left: 4px solid #10B981;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .navigation {
                display: flex;
                justify-content: center;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Clasificador de Emprendimientos Universitarios - Niza</h1>
        </div>
        
        <div class="step-indicators">
            <div class="step completed">
                <div class="step-circle">1</div>
                <div class="step-label">Datos personales</div>
            </div>
            <div class="step completed">
                <div class="step-circle">2</div>
                <div class="step-label">Información académica</div>
            </div>
            <div class="step completed">
                <div class="step-circle">3</div>
                <div class="step-label">Emprendimiento</div>
            </div>
            <div class="step completed">
                <div class="step-circle">4</div>
                <div class="step-label">Clasificación</div>
            </div>
            <div class="step active">
                <div class="step-circle">5</div>
                <div class="step-label">Resultado</div>
            </div>
        </div>
        
        <div class="success-message">
            <p>¡Análisis completado con éxito! Hemos procesado la información de tu emprendimiento y determinado las clasificaciones Niza más relevantes.</p>
        </div>
        
        <div class="card">
            <h2>Resultados del Análisis</h2>
            <p>Para el emprendimiento <strong>TechSolutions MX</strong>, recomendamos considerar las siguientes clasificaciones Niza para el registro de tu marca:</p>
            
            <div class="class-item">
                <div class="class-title">Clase 9: Aparatos e instrumentos científicos</div>
                <div class="class-description">Software, aplicaciones descargables, programas informáticos, hardware.</div>
                <div class="class-relevance">Relevancia: <span class="highlight">95%</span></div>
            </div>
            
            <div class="class-item">
                <div class="class-title">Clase 42: Servicios científicos y tecnológicos</div>
                <div class="class-description">Diseño y desarrollo de software, consultoría tecnológica, servicios informáticos.</div>
                <div class="class-relevance">Relevancia: <span class="highlight">90%</span></div>
            </div>
            
            <div class="class-item">
                <div class="class-title">Clase 35: Publicidad y negocios</div>
                <div class="class-description">Consultoría empresarial, servicios de gestión comercial, marketing digital.</div>
                <div class="class-relevance">Relevancia: <span class="highlight">75%</span></div>
            </div>
            
            <p><span class="highlight">Nota importante:</span> Estas clasificaciones son recomendaciones basadas en la descripción de tu emprendimiento. Se recomienda consultar con un especialista en propiedad intelectual antes de proceder con el registro de marca.</p>
            
            <div class="navigation">
                <a href="/generar_pdf" class="btn-download">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Descargar resultados en PDF
                </a>
            </div>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <p>Gracias por utilizar nuestro clasificador de emprendimientos. ¡Buena suerte con tu registro de marca!</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)

@app.route('/generar_pdf')
def generar_pdf():
    """
    Genera y descarga un PDF con los resultados del análisis.
    """
    # Obtener datos de la sesión
    paso1_data = session.get('paso1_data', {})
    paso2_data = session.get('paso2_data', {})
    paso3_data = session.get('paso3_data', {})
    paso4_data = session.get('paso4_data', {})
    clasificaciones_niza = session.get('clasificaciones_niza', {})
    
    # Compilar los datos para el PDF
    data = {
        'nombre': paso1_data.get('nombre', 'Usuario'),
        'email': paso1_data.get('email', 'email@ejemplo.com'),
        'edad': paso1_data.get('edad', '25'),
        'universidad': paso1_data.get('universidad', 'Universidad'),
        'carrera': paso2_data.get('carrera', 'Carrera'),
        'semestre': paso2_data.get('semestre', 'Semestre actual'),
        'nombre_emprendimiento': paso3_data.get('nombre_emprendimiento', 'Emprendimiento'),
        'fecha_creacion': paso3_data.get('fecha_creacion', datetime.datetime.now().strftime('%d/%m/%Y')),
        'descripcion': paso3_data.get('descripcion', 'Descripción no disponible.'),
        'clasificaciones': clasificaciones_niza
    }
    
    # Si no hay datos en la sesión o no hay clasificaciones, usar datos de muestra
    if not paso1_data or not paso3_data or not clasificaciones_niza:
        data = get_sample_data()
    
    # Generar el PDF
    pdf_buffer = generate_pdf(data)
    
    # Crear una respuesta con el PDF
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=resultados_clasificacion_niza.pdf'
    
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)