import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import time
import random
from datetime import datetime
from clasificacion_niza import obtener_clasificacion_ejemplo
from niza_info import obtener_info_niza, obtener_ejemplos_marcas_por_clase
from utils import validar_datos, validar_email, validar_numero, limpiar_texto, formatear_nombre

# Importar functions para base de datos
from db_manager import guardar_datos_db as guardar_datos
from db_manager import cargar_datos_db as cargar_datos

# Configuración de la página
st.set_page_config(
    page_title="Clasificador de Emprendimientos - Niza",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar CSS personalizado
def cargar_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

cargar_css()

# Inicializar el estado de la sesión si no existe
if 'paso_actual' not in st.session_state:
    st.session_state.paso_actual = 1

if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = {
        'nombre': '',
        'email': '',
        'edad': '',
        'universidad': '',
        'carrera': '',
        'semestre': '',
        'experiencia_previa': '',
        'nombre_emprendimiento': '',
        'descripcion_emprendimiento': '',
        'clasificaciones_niza': None,
        'fecha_registro': pd.Timestamp.now(),
        'acepta_politica': False  # Nuevo campo para aceptación de política
    }

if 'enviado' not in st.session_state:
    st.session_state.enviado = False

if 'mostrar_detalle_clase' not in st.session_state:
    st.session_state.mostrar_detalle_clase = None

if 'modelo_ia_actual' not in st.session_state:
    st.session_state.modelo_ia_actual = "Hugging Face"

# Función para avanzar al siguiente paso
def siguiente_paso():
    # Validar datos del paso actual
    paso_actual = st.session_state.paso_actual
    
    if paso_actual == 1:
        if not validar_datos(st.session_state.datos_usuario, ['nombre', 'email', 'edad', 'universidad']):
            st.error("Por favor, completa todos los campos obligatorios.")
            return
        
        # Validar formato de email
        if not validar_email(st.session_state.datos_usuario['email']):
            st.error("Por favor, ingresa un email válido.")
            return
        
        # Formatear nombre
        st.session_state.datos_usuario['nombre'] = formatear_nombre(st.session_state.datos_usuario['nombre'])
        
    elif paso_actual == 2:
        if not validar_datos(st.session_state.datos_usuario, ['carrera', 'semestre', 'experiencia_previa']):
            st.error("Por favor, completa todos los campos obligatorios.")
            return
        
    elif paso_actual == 3:
        if not validar_datos(st.session_state.datos_usuario, ['nombre_emprendimiento', 'descripcion_emprendimiento']):
            st.error("Por favor, completa todos los campos obligatorios.")
            return
        
        # Validar longitud de la descripción
        if len(st.session_state.datos_usuario['descripcion_emprendimiento']) < 50:
            st.error("Por favor, proporciona una descripción más detallada de tu emprendimiento (mínimo 50 caracteres).")
            return
    
    # Si todo está correcto, avanzar al siguiente paso
    st.session_state.paso_actual += 1

# Función para retroceder al paso anterior
def paso_anterior():
    st.session_state.paso_actual -= 1

# Función para enviar los datos
def enviar_datos():
    # Obtener clasificaciones Niza si aún no se han obtenido
    if not st.session_state.datos_usuario['clasificaciones_niza']:
        with st.spinner('Analizando tu emprendimiento para determinar las clasificaciones Niza apropiadas...'):
            descripcion = st.session_state.datos_usuario['descripcion_emprendimiento']
            try:
                if st.session_state.modelo_ia_actual == "Hugging Face":
                    from llm_huggingface import obtener_clasificaciones_niza_hf
                    clasificaciones = obtener_clasificaciones_niza_hf(descripcion)
                elif st.session_state.modelo_ia_actual == "Modo Ejemplo":
                    clasificaciones = obtener_clasificacion_ejemplo()
                
                # Si hay error, usar clasificaciones de ejemplo
                if clasificaciones and "Error" in clasificaciones.get('clasificaciones', [{}])[0].get('clase', ''):
                    clasificaciones = obtener_clasificacion_ejemplo()
                
                st.session_state.datos_usuario['clasificaciones_niza'] = clasificaciones
            except Exception as e:
                st.error(f"Error al analizar: {str(e)}")
                clasificaciones = obtener_clasificacion_ejemplo()
                st.session_state.datos_usuario['clasificaciones_niza'] = clasificaciones
    
    # Guardar los datos
    try:
        guardar_datos(st.session_state.datos_usuario)
        st.session_state.enviado = True
        st.session_state.paso_actual = 5  # Mostrar el dashboard
    except Exception as e:
        st.error(f"Error al guardar datos: {str(e)}")
        # Continuar a la página de estadísticas de todos modos
        st.session_state.enviado = True
        st.session_state.paso_actual = 5

# Función para mostrar el detalle de una clase Niza
def mostrar_detalle_clase(clase):
    st.session_state.mostrar_detalle_clase = clase

# Función para obtener detalles y ejemplos de una clase Niza
def obtener_detalle_clase(clase):
    info_niza = obtener_info_niza()
    ejemplos_marcas = obtener_ejemplos_marcas_por_clase()
    
    if clase in info_niza:
        return {
            "info": info_niza[clase],
            "ejemplos_marcas": ejemplos_marcas.get(clase, [])
        }
    return None

# Barra de navegación superior
def mostrar_barra_navegacion():
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
        <div>
            <h1 class="main-title">Clasificador de Emprendimientos Universitarios</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Barra lateral
def mostrar_sidebar():
    with st.sidebar:
        st.markdown("# 📝 Niza")
        st.markdown("### Sistema de Clasificación Niza")
        
        # Progreso
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-title">Tu progreso</p>', unsafe_allow_html=True)
        progreso = st.progress(st.session_state.paso_actual / 5)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botones de navegación
        if st.session_state.paso_actual > 1:
            if st.button("⬅️ Paso Anterior", key="btn_anterior"):
                paso_anterior()
                st.rerun()
        
        # Mostrar opciones de IA en paso 4
        if st.session_state.paso_actual == 4:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            st.markdown('<p class="sidebar-title">Opciones de IA</p>', unsafe_allow_html=True)
            ia_option = st.radio(
                "Servicio para análisis de clasificación:",
                ["Hugging Face", "Modo Ejemplo"],
                index=["Hugging Face", "Modo Ejemplo"].index(st.session_state.modelo_ia_actual if st.session_state.modelo_ia_actual in ["Hugging Face", "Modo Ejemplo"] else "Hugging Face"),
                key="ia_option"
            )
            st.session_state.modelo_ia_actual = ia_option
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Información sobre Clasificación Niza
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-title">¿Qué es la Clasificación Niza?</p>', unsafe_allow_html=True)
        st.markdown("""
        La Clasificación Niza es un sistema internacional que clasifica productos y servicios para el registro de marcas.
        
        Organiza todo en 45 clases:
        - Clases 1-34: Productos
        - Clases 35-45: Servicios
        
        Es esencial seleccionar las clases correctas al registrar tu marca para obtener la protección adecuada.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enlace a documentos oficiales
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-title">Enlaces útiles</p>', unsafe_allow_html=True)
        st.markdown("[Clasificación Niza Oficial (WIPO)](https://www.wipo.int/classifications/nice/es/)")
        st.markdown("[IMPI México](https://www.gob.mx/impi)")
        st.markdown('</div>', unsafe_allow_html=True)

# Paso 1: Recolección de datos personales básicos
def mostrar_paso_1():
    # Título y subtítulo
    st.markdown('<h2 class="step-title">Paso 1: Información Personal</h2>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Para comenzar, por favor comparte tus datos personales básicos.</p>', unsafe_allow_html=True)
    
    # Indicador de pasos del wizard
    st.markdown('''
    <div class="wizard-progress">
        <div class="step-indicator active">1<span class="step-label">Datos personales</span></div>
        <div class="step-indicator">2<span class="step-label">Información académica</span></div>
        <div class="step-indicator">3<span class="step-label">Emprendimiento</span></div>
        <div class="step-indicator">4<span class="step-label">Clasificación</span></div>
        <div class="step-indicator">5<span class="step-label">Resultado</span></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Crear tarjeta para el formulario
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre Completo *", 
                             value=st.session_state.datos_usuario['nombre'],
                             placeholder="Ej. Juan Pérez García",
                             key="nombre_input")
        st.session_state.datos_usuario['nombre'] = nombre
        
        email = st.text_input("Correo Electrónico *", 
                            value=st.session_state.datos_usuario['email'],
                            placeholder="tu.email@universidad.edu",
                            key="email_input")
        st.session_state.datos_usuario['email'] = email
    
    with col2:
        edad = st.number_input("Edad *", 
                             min_value=16, max_value=80, 
                             value=int(st.session_state.datos_usuario['edad']) if st.session_state.datos_usuario['edad'] else 18,
                             key="edad_input")
        st.session_state.datos_usuario['edad'] = str(edad)
        
        universidad = st.text_input("Universidad *", 
                                 value=st.session_state.datos_usuario['universidad'],
                                 placeholder="Nombre de tu universidad",
                                 key="universidad_input")
        st.session_state.datos_usuario['universidad'] = universidad
    
    # Navegación del wizard - solo botón de continuar en el primer paso
    st.markdown('<div class="wizard-navigation">', unsafe_allow_html=True)
    st.markdown('<div style="flex: 1;"></div>', unsafe_allow_html=True)  # Espacio a la izquierda
    continuar_btn = st.button("Continuar →", key="btn_siguiente_1", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Información sobre la recolección de datos
    with st.expander("Información sobre la recolección de datos"):
        st.markdown("""
        Esta información nos ayuda a comprender mejor las características de los emprendedores universitarios 
        y mejorar nuestras recomendaciones de clasificación Niza. Todos los datos son procesados de manera 
        anónima para fines estadísticos.
        
        Al final del proceso, se te pedirá aceptar nuestra política de privacidad antes de enviar tus datos.
        """)
    
    if continuar_btn:
        siguiente_paso()
        st.rerun()

# Paso 2: Información académica y experiencia
def mostrar_paso_2():
    # Título y subtítulo
    st.markdown('<h2 class="step-title">Paso 2: Información Académica</h2>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Cuéntanos más sobre tus estudios y experiencia previa.</p>', unsafe_allow_html=True)
    
    # Indicador de pasos del wizard
    st.markdown('''
    <div class="wizard-progress">
        <div class="step-indicator completed">1<span class="step-label">Datos personales</span></div>
        <div class="step-indicator active">2<span class="step-label">Información académica</span></div>
        <div class="step-indicator">3<span class="step-label">Emprendimiento</span></div>
        <div class="step-indicator">4<span class="step-label">Clasificación</span></div>
        <div class="step-indicator">5<span class="step-label">Resultado</span></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Crear tarjeta para el formulario
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        carrera = st.text_input("Carrera o Programa Académico *", 
                              value=st.session_state.datos_usuario['carrera'],
                              placeholder="Ej. Ingeniería, Derecho, Administración",
                              key="carrera_input")
        st.session_state.datos_usuario['carrera'] = carrera
        
        semestre = st.selectbox("Semestre Actual *", 
                             options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Egresado"],
                             index=0 if not st.session_state.datos_usuario['semestre'] else 
                                  ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Egresado"].index(st.session_state.datos_usuario['semestre']),
                             key="semestre_input")
        st.session_state.datos_usuario['semestre'] = semestre
    
    with col2:
        st.write("&nbsp;") # Espacio en blanco para alineación
        experiencia = st.radio("¿Tienes experiencia previa emprendiendo? *", 
                             options=["Sí", "No"],
                             index=0 if st.session_state.datos_usuario['experiencia_previa'] == "Sí" else 1,
                             key="experiencia_input",
                             horizontal=True)
        st.session_state.datos_usuario['experiencia_previa'] = experiencia
        
        if experiencia == "Sí":
            st.text_area("Cuéntanos brevemente sobre tu experiencia anterior", 
                       placeholder="Describe brevemente tu experiencia emprendiendo...",
                       height=100,
                       key="experiencia_detalle_input")
    
    # Navegación del wizard
    st.markdown('<div class="wizard-navigation">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        anterior_btn = st.button("← Anterior", key="btn_anterior_2")
    with col2:
        continuar_btn = st.button("Continuar →", key="btn_siguiente_2", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Información adicional
    with st.expander("Importancia del perfil académico en el emprendimiento"):
        st.markdown("""
        Tu perfil académico puede influir en cómo enfocas tu emprendimiento:
        
        - **Negocios/Administración**: Suelen tener ventaja en aspectos financieros y de gestión
        - **Ingenierías/Ciencias**: A menudo destacan en innovación técnica y desarrollo de productos
        - **Humanidades/Ciencias Sociales**: Aportan perspectivas valiosas centradas en el usuario
        
        No hay un perfil "ideal" para emprender - ¡la diversidad de formaciones enriquece el ecosistema emprendedor!
        """)
    
    if anterior_btn:
        paso_anterior()
        st.rerun()
    
    if continuar_btn:
        siguiente_paso()
        st.rerun()

# Paso 3: Información del emprendimiento
def mostrar_paso_3():
    # Título y subtítulo
    st.markdown('<h2 class="step-title">Paso 3: Información del Emprendimiento</h2>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Cuéntanos sobre tu proyecto o idea de negocio.</p>', unsafe_allow_html=True)
    
    # Indicador de pasos del wizard
    st.markdown('''
    <div class="wizard-progress">
        <div class="step-indicator completed">1<span class="step-label">Datos personales</span></div>
        <div class="step-indicator completed">2<span class="step-label">Información académica</span></div>
        <div class="step-indicator active">3<span class="step-label">Emprendimiento</span></div>
        <div class="step-indicator">4<span class="step-label">Clasificación</span></div>
        <div class="step-indicator">5<span class="step-label">Resultado</span></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Crear tarjeta para el formulario
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    
    nombre_emprendimiento = st.text_input("Nombre del Emprendimiento o Proyecto *", 
                                      value=st.session_state.datos_usuario['nombre_emprendimiento'],
                                      placeholder="Ej. EcoSolutions, TechInnovate, etc.",
                                      key="nombre_emprendimiento_input")
    st.session_state.datos_usuario['nombre_emprendimiento'] = nombre_emprendimiento
    
    st.markdown('<p style="margin-top: 20px; margin-bottom: 5px;"><strong>Descripción detallada del emprendimiento *</strong></p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-top: 0; margin-bottom: 10px; font-size: 0.9rem; color: #6B7280;">Describe con detalle los productos o servicios que ofreces o planeas ofrecer. Incluye información sobre tu público objetivo, canales de distribución y cualquier aspecto relevante.</p>', unsafe_allow_html=True)
    
    descripcion = st.text_area("", 
                            value=st.session_state.datos_usuario['descripcion_emprendimiento'],
                            placeholder="Describe tu emprendimiento en detalle...\nEjemplo: Mi emprendimiento se dedica al desarrollo de aplicaciones móviles para el sector educativo, específicamente centradas en mejorar la experiencia de aprendizaje de estudiantes universitarios. Nuestros productos incluyen aplicaciones de organización de tareas, herramientas de estudio colaborativo y sistemas de seguimiento de proyectos académicos...",
                            height=200,
                            key="descripcion_emprendimiento_input")
    st.session_state.datos_usuario['descripcion_emprendimiento'] = descripcion
    
    # Contador de caracteres
    st.markdown(f'<p style="text-align: right; font-size: 0.8rem; color: {"#10B981" if len(descripcion) >= 50 else "#EF4444"};">{len(descripcion)}/50 caracteres mínimos</p>', unsafe_allow_html=True)
    
    # Consejos para una buena descripción
    with st.expander("Consejos para una buena descripción"):
        st.markdown("""
        Una descripción detallada nos permite analizar mejor tu emprendimiento y generar clasificaciones Niza más precisas.
        
        **Incluye información sobre:**
        - Productos o servicios específicos que ofreces
        - Tecnologías o métodos que utilizas
        - Público objetivo o clientes potenciales
        - Canales de distribución o venta
        - Elementos diferenciadores de tu propuesta
        
        **Evita:**
        - Descripciones muy genéricas o ambiguas
        - Centrarte solo en la misión/visión sin describir los productos/servicios reales
        - Usar jerga técnica sin explicar su significado
        """)
    
    # Navegación del wizard
    st.markdown('<div class="wizard-navigation">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        anterior_btn = st.button("← Anterior", key="btn_anterior_3")
    with col2:
        continuar_btn = st.button("Continuar →", key="btn_siguiente_3", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if anterior_btn:
        paso_anterior()
        st.rerun()
    
    if continuar_btn:
        siguiente_paso()
        st.rerun()

# Paso 4: Clasificación Niza
def mostrar_paso_4():
    # Título y subtítulo
    st.markdown('<h2 class="step-title">Paso 4: Clasificación Niza de tu Emprendimiento</h2>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Revisa las clasificaciones sugeridas para proteger tu marca.</p>', unsafe_allow_html=True)
    
    # Indicador de pasos del wizard
    st.markdown('''
    <div class="wizard-progress">
        <div class="step-indicator completed">1<span class="step-label">Datos personales</span></div>
        <div class="step-indicator completed">2<span class="step-label">Información académica</span></div>
        <div class="step-indicator completed">3<span class="step-label">Emprendimiento</span></div>
        <div class="step-indicator active">4<span class="step-label">Clasificación</span></div>
        <div class="step-indicator">5<span class="step-label">Resultado</span></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Crear tarjeta para el contenido
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    
    # Si aún no se ha generado la clasificación, generarla
    if not st.session_state.datos_usuario['clasificaciones_niza']:
        with st.spinner('Analizando tu emprendimiento para determinar las clasificaciones Niza apropiadas...'):
            descripcion = st.session_state.datos_usuario['descripcion_emprendimiento']
            try:
                if st.session_state.modelo_ia_actual == "Hugging Face":
                    from llm_huggingface import obtener_clasificaciones_niza_hf
                    clasificaciones = obtener_clasificaciones_niza_hf(descripcion)
                elif st.session_state.modelo_ia_actual == "Modo Ejemplo":
                    clasificaciones = obtener_clasificacion_ejemplo()
                
                # Si hay error, usar clasificaciones de ejemplo
                if clasificaciones and "Error" in clasificaciones.get('clasificaciones', [{}])[0].get('clase', ''):
                    clasificaciones = obtener_clasificacion_ejemplo()
                
                st.session_state.datos_usuario['clasificaciones_niza'] = clasificaciones
            except Exception as e:
                st.error(f"Error al analizar: {str(e)}")
                clasificaciones = obtener_clasificacion_ejemplo()
                st.session_state.datos_usuario['clasificaciones_niza'] = clasificaciones
    
    # Mostrar las clasificaciones
    clasificaciones = st.session_state.datos_usuario['clasificaciones_niza']
    
    if clasificaciones and 'clasificaciones' in clasificaciones:
        # Mostrar resumen del emprendimiento
        st.markdown('<h3 style="color: #4F46E5; margin-bottom: 15px;">Resumen del Emprendimiento</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="background-color: #EEF2FF; padding: 15px; border-radius: 8px; border-left: 4px solid #4F46E5;">{clasificaciones.get("resumen", "Resumen no disponible")}</p>', unsafe_allow_html=True)
        
        # Mostrar clasificaciones recomendadas
        st.markdown('<h3 style="color: #4F46E5; margin-top: 25px; margin-bottom: 15px;">Clasificaciones Niza Recomendadas</h3>', unsafe_allow_html=True)
        
        for i, clasificacion in enumerate(clasificaciones['clasificaciones']):
            # Determinar nivel de confianza para el badge
            confianza = clasificacion.get('confianza')
            # Convertir confianza a float
            if isinstance(confianza, str):
                confianza = confianza.replace(',', '.')
                confianza = float(confianza)
            
            if confianza >= 0.7:
                confianza_clase = "high"
                confianza_texto = "Alta"
            elif confianza >= 0.4:
                confianza_clase = "medium"
                confianza_texto = "Media"
            else:
                confianza_clase = "low"
                confianza_texto = "Baja"
                
            # Crear tarjeta para cada clasificación
            st.markdown(f'''
            <div class="clasificacion-card">
                <div class="clasificacion-header">
                    <h3>Clase {clasificacion['clase']}: {clasificacion['descripcion']}</h3>
                    <span class="confianza-badge {confianza_clase}">Relevancia {confianza_texto}</span>
                </div>
                <p>{clasificacion['descripcion']}</p>
                <button 
                    onclick="parent.postMessage({{type: 'streamlit:buttonClicked', id: 'btn_detalle_clase_{clasificacion['clase']}'}}, '*')"
                    style="background-color: #F3F4F6; color: #4B5563; border: 1px solid #D1D5DB; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 0.9rem;"
                >
                    Ver detalles y ejemplos
                </button>
            </div>
            ''', unsafe_allow_html=True)
            
            # Botón oculto que captura el clic
            if st.button(f"btn_detalle_clase_{clasificacion['clase']}", key=f"btn_detalle_clase_{clasificacion['clase']}", help="Ver detalles y ejemplos de esta clase Niza"):                                                                                                 
                mostrar_detalle_clase(clasificacion['clase'])
                st.rerun()
    
    # Mostrar detalle de una clase específica
    if st.session_state.mostrar_detalle_clase:
        clase = st.session_state.mostrar_detalle_clase
        detalle = obtener_detalle_clase(clase)
        
        if detalle:
            with st.expander(f"Detalles de la Clase {clase}", expanded=True):
                st.markdown(f"### Clase {clase}: {detalle['info']['titulo']}")
                st.markdown("#### Descripción completa:")
                st.markdown(detalle['info']['descripcion_completa'])
                
                st.markdown("#### Esta clase incluye principalmente:")
                for item in detalle['info']['incluye']:
                    st.markdown(f"- {item}")
                
                st.markdown("#### Esta clase no incluye:")
                for item in detalle['info']['no_incluye']:
                    st.markdown(f"- {item}")
                
                if detalle['ejemplos_marcas']:
                    st.markdown("#### Ejemplos de marcas en esta clasificación:")
                    marcas_texto = ", ".join(detalle['ejemplos_marcas'])
                    st.markdown(f"<p style='color: #4F46E5;'>{marcas_texto}</p>", unsafe_allow_html=True)
        
        # Botón para cerrar detalles
        if st.button("← Volver a la lista de clasificaciones", key="btn_cerrar_detalle"):
            st.session_state.mostrar_detalle_clase = None
            st.rerun()
    
    # Sección de política de privacidad y aceptación
    st.markdown('<div class="privacy-policy">', unsafe_allow_html=True)
    st.markdown('<h3>Política de Privacidad y Protección de Datos</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Política de Privacidad
    
    Esta aplicación recopila datos de emprendedores universitarios con el fin de:
    
    1. Generar clasificaciones Niza precisas para tus productos o servicios
    2. Crear estadísticas agregadas sobre el ecosistema emprendedor universitario
    3. Mejorar nuestras recomendaciones basadas en patrones identificados
    
    **Tus datos están protegidos.** No compartimos información personal con terceros y cumplimos con la legislación de protección de datos vigente. 
    Los resultados estadísticos se presentan siempre de forma agregada y anónima.
    
    Si deseas que eliminemos tus datos de nuestro sistema en cualquier momento, puedes solicitarlo enviando un correo a privacidad@ejemplo.com.
    """)
    
    # Checkbox de aceptación
    st.markdown('<div class="privacy-checkbox">', unsafe_allow_html=True)
    acepta = st.checkbox("Acepto la política de privacidad y el procesamiento de mis datos para los fines descritos", 
                       value=st.session_state.datos_usuario.get('acepta_politica', False),
                       key="acepta_input")
    st.session_state.datos_usuario['acepta_politica'] = acepta
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navegación del wizard
    st.markdown('<div class="wizard-navigation">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        anterior_btn = st.button("← Anterior", key="btn_anterior_4")
    with col2:
        continuar_btn = st.button("Finalizar y Ver Estadísticas", key="btn_siguiente_4", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if anterior_btn:
        paso_anterior()
        st.rerun()
    
    if continuar_btn and st.session_state.datos_usuario.get('acepta_politica', False):
        enviar_datos()
        st.rerun()

# Paso 5: Dashboard de estadísticas
def mostrar_paso_5():
    # Título y subtítulo
    st.markdown('<h2 class="step-title">Estadísticas de Emprendedores Universitarios</h2>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Análisis de datos recopilados sobre emprendimientos universitarios.</p>', unsafe_allow_html=True)
    
    # Indicador de pasos del wizard
    st.markdown('''
    <div class="wizard-progress">
        <div class="step-indicator completed">1<span class="step-label">Datos personales</span></div>
        <div class="step-indicator completed">2<span class="step-label">Información académica</span></div>
        <div class="step-indicator completed">3<span class="step-label">Emprendimiento</span></div>
        <div class="step-indicator completed">4<span class="step-label">Clasificación</span></div>
        <div class="step-indicator active">5<span class="step-label">Resultado</span></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Cargar datos para el dashboard
    df = cargar_datos()
    
    if df.empty:
        st.warning("Aún no hay suficientes datos para generar estadísticas. ¡Sé el primero en completar el formulario!")
    else:
        st.success(f"Analizando datos de {len(df)} emprendedores universitarios")
        
        # Dashboard principal
        st.markdown('<div class="dashboard-container fade-in">', unsafe_allow_html=True)
        
        # Sección superior - Métricas clave
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Emprendedores", len(df))
        
        with col2:
            promedio_edad = round(df['edad'].astype(float).mean(), 1)
            st.metric("Edad Promedio", promedio_edad)
        
        with col3:
            pct_experiencia = round(100 * df['experiencia_previa'].value_counts().get('Sí', 0) / len(df), 1)
            st.metric("% Con Experiencia Previa", f"{pct_experiencia}%")
        
        with col4:
            universidades = df['universidad'].nunique()
            st.metric("Universidades Representadas", universidades)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sección de gráficos
        st.markdown('<div class="dashboard-container fade-in" style="margin-top: 20px;">', unsafe_allow_html=True)
        
        # Primera fila de gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center; color: #FF4B4B; font-size: 1.2rem;">Distribución por Universidad</h3>', unsafe_allow_html=True)
            fig_uni = px.pie(df, names='universidad', hole=0.4, 
                           color_discrete_sequence=px.colors.sequential.RdBu)
            fig_uni.update_traces(textposition='inside', textinfo='percent+label')
            fig_uni.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_uni, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center; color: #FF4B4B; font-size: 1.2rem;">Distribución por Edad</h3>', unsafe_allow_html=True)
            fig_edad = px.histogram(df, x='edad', nbins=12, 
                                  color_discrete_sequence=['#FF4B4B'])
            fig_edad.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_edad, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Segunda fila de gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center; color: #FF4B4B; font-size: 1.2rem;">Experiencia Previa Emprendiendo</h3>', unsafe_allow_html=True)
            fig_exp = px.pie(df, names='experiencia_previa', hole=0.6,
                           color_discrete_sequence=px.colors.sequential.Reds)
            fig_exp.update_traces(textposition='inside', textinfo='percent+label')
            fig_exp.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_exp, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center; color: #FF4B4B; font-size: 1.2rem;">Top 5 Carreras</h3>', unsafe_allow_html=True)
            
            if 'carrera' in df.columns:
                top_carreras = df['carrera'].value_counts().head(5)
                fig_carrera = px.bar(top_carreras, 
                                  color_discrete_sequence=['#FF4B4B', '#FF6B6B', '#FF8B8B', '#FFA9A9', '#FFC7C7'])
                fig_carrera.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
                st.plotly_chart(fig_carrera, use_container_width=True)
            else:
                st.info("No hay datos disponibles sobre carreras")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Clasificaciones Niza
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #FF4B4B; font-size: 1.2rem;">Clasificaciones Niza más comunes</h3>', unsafe_allow_html=True)
        
        # Extraer y contar las clasificaciones más comunes
        clases_niza = []
        for _, row in df.iterrows():
            if row.get('clasificaciones_niza') and isinstance(row['clasificaciones_niza'], dict) and 'clasificaciones' in row['clasificaciones_niza']:
                for clasificacion in row['clasificaciones_niza']['clasificaciones']:
                    if isinstance(clasificacion, dict) and 'clase' in clasificacion:
                        clases_niza.append(str(clasificacion['clase']))
        
        if clases_niza:
            clases_count = pd.Series(clases_niza).value_counts().head(10)
            fig_niza = px.bar(clases_count, 
                            color_discrete_sequence=px.colors.sequential.RdBu)
            fig_niza.update_layout(xaxis_title="Clase Niza", yaxis_title="Frecuencia",
                                 margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_niza, use_container_width=True)
        else:
            st.info("Aún no hay suficientes datos de clasificaciones Niza para mostrar estadísticas.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Información de base de datos
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #0275d8; font-size: 1.2rem;">Almacenamiento Seguro</h3>', unsafe_allow_html=True)
        st.markdown("Los datos se almacenan en una base de datos PostgreSQL para mayor seguridad y escalabilidad.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="background-color: #d4edda; padding: 15px; border-radius: 10px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #155724; font-size: 1.2rem;">Modelos de IA</h3>', unsafe_allow_html=True)
        st.markdown("Esta aplicación utiliza el modelo Mixtral 8x7B de Hugging Face para un análisis preciso de clasificaciones Niza, con descripciones detalladas de las 45 clases.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para comenzar de nuevo
    st.markdown('<div style="margin-top: 20px; text-align: center;">', unsafe_allow_html=True)
    if st.button("Comenzar Nuevo Registro", key="btn_reiniciar", type="primary"):
        st.session_state.paso_actual = 1
        st.session_state.datos_usuario = {
            'nombre': '',
            'email': '',
            'edad': '',
            'universidad': '',
            'carrera': '',
            'semestre': '',
            'experiencia_previa': '',
            'nombre_emprendimiento': '',
            'descripcion_emprendimiento': '',
            'clasificaciones_niza': None,
            'fecha_registro': pd.Timestamp.now()
        }
        st.session_state.enviado = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Función principal para mostrar la aplicación
def main():
    mostrar_barra_navegacion()
    mostrar_sidebar()
    
    if st.session_state.paso_actual == 1:
        mostrar_paso_1()
    elif st.session_state.paso_actual == 2:
        mostrar_paso_2()
    elif st.session_state.paso_actual == 3:
        mostrar_paso_3()
    elif st.session_state.paso_actual == 4:
        mostrar_paso_4()
    elif st.session_state.paso_actual == 5:
        mostrar_paso_5()

if __name__ == "__main__":
    main()