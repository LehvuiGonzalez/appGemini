import streamlit as st
import re

def validar_nombre(nombre):
    """Valida si un nombre solo contiene caracteres alfabéticos e inicia con mayúscula.

    Args:
        nombre: El nombre a validar.

    Returns:
        bool: True si el nombre es válido, False si no lo es.
    """
    patron = r"^[A-Z][a-zA-Z]+$"
    return re.match(patron, nombre) is not None

def validar_email(email):
    """Valida una dirección de correo electrónico.

    Args:
        email: La dirección de correo electrónico a validar.

    Returns:
        bool: True si el email es válido, False si no lo es.
    """
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    """Valida un número de teléfono (ejemplo: +57 311 234 5678).

    Args:
        telefono: El número de teléfono a validar.

    Returns:
        bool: True si el teléfono es válido, False si no lo es.
    """
    patron = r"^\+\d{2} \d{3} \d{3} \d{4}$"
    return re.match(patron, telefono) is not None

def validar_fecha(fecha):
    """Valida una fecha en formato DD/MM/AAAA.

    Args:
        fecha: La fecha a validar.

    Returns:
        bool: True si la fecha es válida, False si no lo es.
    """
    patron = r"^\d{2}/\d{2}/\d{4}$"
    return re.match(patron, fecha) is not None

# Interfaz de usuario con Streamlit
st.title("Formulario de Validación")

nombre = st.text_input("Nombre:")
email = st.text_input("Correo electrónico:")
telefono = st.text_input("Número de teléfono:")
fecha = st.text_input("Fecha (DD/MM/AAAA):")

if st.button("Validar"):
    if validar_nombre(nombre):
        st.success("Nombre válido.")
    else:
        st.error("Nombre inválido. Solo se permiten caracteres alfabéticos e iniciar con mayúscula.")

    if validar_email(email):
        st.success("Correo electrónico válido.")
    else:
        st.error("Correo electrónico inválido.")

    if validar_telefono(telefono):
        st.success("Número de teléfono válido.")
    else:
        st.error("Número de teléfono inválido. Ejemplo: +57 311 234 5678")

    if validar_fecha(fecha):
        st.success("Fecha válida.")
    else:
        st.error("Fecha inválida. Formato DD/MM/AAAA")
