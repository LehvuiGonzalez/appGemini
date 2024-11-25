import streamlit as st
import re

def evaluar_contrasena(contrasena):
    """Evalúa la fortaleza de una contraseña y devuelve un mensaje.

    Args:
        contrasena: La contraseña a evaluar.

    Returns:
        str: Un mensaje indicando la fortaleza de la contraseña y sugerencias.
    """

    # Expresiones regulares para cada criterio
    mayusculas = re.compile(r'[A-Z]')
    minusculas = re.compile(r'[a-z]')
    numeros = re.compile(r'\d')
    especiales = re.compile(r'[^A-Za-z0-9]')

    # Validación de cada criterio
    tiene_mayusculas = mayusculas.search(contrasena) is not None
    tiene_minusculas = minusculas.search(contrasena) is not None
    tiene_numeros = numeros.search(contrasena) is not None
    tiene_especiales = especiales.search(contrasena) is not None
    es_suficientemente_larga = len(contrasena) >= 8

    # Mensaje y sugerencias
    if all([tiene_mayusculas, tiene_minusculas, tiene_numeros, tiene_especiales, es_suficientemente_larga]):
        return "¡Excelente! Tu contraseña es muy segura."
    else:
        sugerencias = []
        if not es_suficientemente_larga:
            sugerencias.append("La contraseña debe tener al menos 8 caracteres.")
        if not tiene_mayusculas:
            sugerencias.append("Incluye al menos una letra mayúscula.")
        if not tiene_minusculas:
            sugerencias.append("Incluye al menos una letra minúscula.")
        if not tiene_numeros:
            sugerencias.append("Incluye al menos un número.")
        if not tiene_especiales:
            sugerencias.append("Incluye al menos un carácter especial.")
        return f"Tu contraseña podría ser más segura. Te sugerimos: {', '.join(sugerencias)}"

# Interfaz de usuario con Streamlit
st.title("Evaluador de Contraseñas")
contrasena = st.text_input("Ingrese su contraseña:")

if contrasena:
    resultado = evaluar_contrasena(contrasena)
    st.write(resultado)
