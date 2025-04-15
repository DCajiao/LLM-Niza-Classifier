import streamlit as st

# Configuración básica de la página
st.set_page_config(
    page_title="Prueba Streamlit",
    page_icon="🧪",
    layout="wide"
)

# Título principal
st.title("Prueba de Streamlit")

# Un texto simple
st.write("Esta es una aplicación de prueba para verificar que Streamlit funciona correctamente.")

# Un widget simple
name = st.text_input("Escribe tu nombre:")
if name:
    st.write(f"¡Hola, {name}!")

# Un botón simple
if st.button("Haz clic"):
    st.balloons()
    st.success("¡El botón funciona correctamente!")

# Mostrar información sobre la ejecución
st.info("Si puedes ver esta aplicación, significa que Streamlit está funcionando correctamente en tu entorno.")