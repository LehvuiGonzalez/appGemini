import streamlit as st
import re
import PyPDF2  # Asegúrate de instalar esta biblioteca: pip install PyPDF2

# Función para buscar palabras/frases en el texto y proporcionar contexto
def buscar_contexto(texto, palabra, contexto=30):
    # Crear una expresión regular para encontrar la palabra con contexto
    patron = rf"(.{{0,{contexto}}}{re.escape(palabra)}.{{0,{contexto}}})"
    coincidencias = re.findall(patron, texto, re.IGNORECASE)
    return coincidencias

# Función para extraer texto de un archivo PDF
def extraer_texto_pdf(archivo):
    texto = ""
    pdf_reader = PyPDF2.PdfReader(archivo)
    for pagina in pdf_reader.pages:
        texto += pagina.extract_text()
    return texto

# Título de la app
st.title("Buscador con contexto en libros y documentos PDF")

# Subir un archivo de texto o PDF
archivo_subido = st.file_uploader("Sube un archivo de texto (.txt) o PDF (.pdf)", type=["txt", "pdf"])

if archivo_subido:
    # Determinar el tipo de archivo y extraer texto
    if archivo_subido.name.endswith(".txt"):
        texto = archivo_subido.read().decode("utf-8")
    elif archivo_subido.name.endswith(".pdf"):
        texto = extraer_texto_pdf(archivo_subido)
    else:
        texto = ""
    
    if texto:
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
    else:
        st.error("No se pudo extraer el texto del archivo.")
