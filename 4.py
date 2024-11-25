import streamlit as st
import re

# Título de la aplicación
st.title("Buscador de Patrones en Textos")

# Información sobre el autor
st.write("Autor: Lehvui González Cardona")

# Explicación de la aplicación
st.write("""
    Esta aplicación te permite cargar un archivo de texto o ingresar texto manualmente.
    Puedes buscar patrones específicos utilizando expresiones regulares.
""")

# Opción de ingresar texto manualmente o cargar archivo
opcion = st.selectbox("¿Cómo quieres ingresar el texto?", ["Ingresar texto manualmente", "Cargar archivo de texto"])

# Variable para almacenar el texto
texto = ""

if opcion == "Ingresar texto manualmente":
    texto = st.text_area("Escribe el texto aquí:")

elif opcion == "Cargar archivo de texto":
    archivo = st.file_uploader("Sube un archivo de texto (.txt)", type=["txt"])
    if archivo is not None:
        texto = archivo.read().decode("utf-8")

# Input para definir la expresión regular
patron = st.text_input("Ingresa la expresión regular que quieres buscar:")

# Función para buscar patrones en el texto
def buscar_patron(texto, patron):
    try:
        coincidencias = re.findall(patron, texto)
        return coincidencias
    except re.error:
        st.error("La expresión regular no es válida.")
        return []

# Si hay texto y patrón, hacer la búsqueda
if texto and patron:
    resultados = buscar_patron(texto, patron)
    if resultados:
        st.success(f"Se encontraron {len(resultados)} coincidencia(s) para el patrón '{patron}':")
        st.write(resultados)
    else:
        st.error("No se encontraron coincidencias.")
