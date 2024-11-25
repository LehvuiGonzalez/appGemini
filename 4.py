import streamlit as st
import requests
import re

# Función para buscar palabras/frases en el texto y proporcionar contexto
def buscar_contexto(texto, palabra, contexto=30):
    patron = rf"(.{{0,{contexto}}}{re.escape(palabra)}.{{0,{contexto}}})"
    coincidencias = re.findall(patron, texto, re.IGNORECASE)
    return coincidencias

# Función para buscar libros usando Google Books API
def buscar_libros(consulta):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": consulta, "maxResults": 5}  # Cambia maxResults si quieres más resultados
    respuesta = requests.get(url, params=params)
    if respuesta.status_code == 200:
        return respuesta.json()["items"]
    return None

# Función para descargar contenido del libro (si está disponible)
def obtener_contenido_libro(libro_id):
    url = f"https://www.googleapis.com/books/v1/volumes/{libro_id}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        libro = respuesta.json()
        if "textSnippet" in libro.get("searchInfo", {}):
            return libro["searchInfo"]["textSnippet"]
        elif "description" in libro.get("volumeInfo", {}):
            return libro["volumeInfo"]["description"]
    return "No se pudo obtener contenido para este libro."

# Título de la app
st.title("Buscador de contexto en libros online")

# Entrada para buscar libros
consulta = st.text_input("Busca un libro por título, autor o palabras clave:")

if consulta:
    # Buscar libros en la web
    libros = buscar_libros(consulta)
    
    if libros:
        st.success(f"Se encontraron {len(libros)} libros. Selecciona uno para buscar:")
        
        # Mostrar los libros encontrados
        opciones = {f"{libro['volumeInfo']['title']} - {libro['volumeInfo'].get('authors', ['Autor desconocido'])[0]}": libro["id"] for libro in libros}
        seleccion = st.selectbox("Selecciona un libro:", list(opciones.keys()))
        
        if seleccion:
            libro_id = opciones[seleccion]
            contenido = obtener_contenido_libro(libro_id)
            
            if contenido:
                # Input para ingresar la palabra o frase de búsqueda
                palabra = st.text_input("Ingresa la palabra o frase que quieres buscar en el libro:")
                
                # Parámetro para definir el tamaño del contexto
                contexto = st.slider("Define el tamaño del contexto (en caracteres):", min_value=10, max_value=100, value=30)
                
                if palabra:
                    # Buscar coincidencias
                    resultados = buscar_contexto(contenido, palabra, contexto)
                    
                    if resultados:
                        st.success(f"Se encontraron {len(resultados)} coincidencia(s) para '{palabra}':")
                        for i, resultado in enumerate(resultados, 1):
                            resultado_resaltado = resultado.replace(palabra, f"**{palabra}**")
                            st.markdown(f"**{i}.** ...{resultado_resaltado}...")
                    else:
                        st.error("No se encontraron coincidencias.")
            else:
                st.error("No se pudo obtener el contenido del libro seleccionado.")
    else:
        st.error("No se encontraron libros. Intenta con otra consulta.")
