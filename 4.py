import streamlit as st
import re

# Función para buscar palabras/frases en el texto y proporcionar contexto
def buscar_contexto(texto, palabra, contexto=30):
    # Crear una expresión regular para encontrar la palabra con contexto
    patron = rf"(.{{0,{contexto}}}{re.escape(palabra)}.{{0,{contexto}}})"
    coincidencias = re.findall(patron, texto, re.IGNORECASE)
    return coincidencias

# Título de la app
st.title("Buscador con contexto en libros")

# Subir un archivo de texto
archivo_subido = st.file_uploader("Sube un archivo de texto (.txt)", type=["txt"])

if archivo_subido:
    # Leer el contenido del archivo
    texto = archivo_subido.read().decode("utf-8")

    # Input para ingresar la palabra o frase de búsqueda
    palabra = st.text_input("Ingresa la palabra o frase que quieres buscar:")

    # Parámetro para definir el tamaño del contexto
    contexto = st.slider("Define el tamaño del contexto (en caracteres):", min_value=10, max_value=100, value=30)

    if palabra:
        # Buscar coincidencias
        resultados = buscar_contexto(texto, palabra, contexto)

        if resultados:
            st.success(f"Se encontraron {len(resultados)} coincidencia(s) para '{palabra}':")
            for i, resultado in enumerate(resultados, 1):
                # Resaltar la palabra en el contexto
                resultado_resaltado = resultado.replace(palabra, f"**{palabra}**")
                st.markdown(f"**{i}.** ...{resultado_resaltado}...")
        else:
            st.error("No se encontraron coincidencias.")
