import streamlit as st
import sys
import os

# Configuración básica de la página
st.set_page_config(
    page_title="App de Depuración",
    page_icon="🔍",
    layout="wide"
)

# Información de diagnóstico
st.title("Aplicación de diagnóstico Streamlit")
st.write("Esta aplicación muestra información sobre el entorno para diagnosticar problemas.")

# Información de versiones
st.header("Información del sistema")
st.write(f"Python versión: {sys.version}")
st.write(f"Streamlit versión: {st.__version__}")
st.write(f"Directorio actual: {os.getcwd()}")

# Mostrar variables de entorno (excluyendo claves sensibles)
st.header("Variables de entorno")
env_vars = {k: "***OCULTO***" if k.lower().endswith(('key', 'token', 'secret', 'password')) else v 
            for k, v in os.environ.items()}
st.json(env_vars)

# Probar funcionalidad de widgets básicos
st.header("Prueba de widgets básicos")
st.write("Si puedes interactuar con estos widgets, la funcionalidad básica de Streamlit está funcionando.")

nombre = st.text_input("Nombre:")
if nombre:
    st.write(f"Hola, {nombre}!")

opcion = st.selectbox("Selecciona una opción:", ["Opción 1", "Opción 2", "Opción 3"])
st.write(f"Seleccionaste: {opcion}")

if st.button("Haz clic aquí"):
    st.success("¡El botón funciona!")
    st.balloons()

# Mostrar una barra de progreso animada
st.header("Prueba de elementos dinámicos")
progress_bar = st.progress(0)
for i in range(100):
    # Actualiza la barra de progreso con cada iteración
    progress_bar.progress(i + 1)
st.success("Completado!")

# Mensaje final
st.info("Si puedes ver esta aplicación y los widgets funcionan, entonces Streamlit está operando correctamente. El problema puede estar en el código específico de tu aplicación principal.")