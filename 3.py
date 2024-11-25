import streamlit as st
import pandas as pd
import requests
import re
import io

# Función para extraer información específica usando regex
def extract_info(row):
    row_text = ' '.join(map(str, row))  # Combinar todos los valores en una fila en un solo texto
    
    # Expresiones regulares para cada tipo de dato
    serial_pattern = r'\b\d{5,7}\b'  # Números de serie (5-7 dígitos)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Correos electrónicos
    phone_pattern = r'\+?\d{1,3}[\s-]?\d{9,12}'  # Teléfonos
    date_pattern = r'\b\d{2}/\d{2}/\d{2}\b'  # Fechas en formato DD/MM/YY
    value_pattern = r'\b\d+(\.\d{1,2})?\b'  # Valores numéricos con hasta dos decimales
    name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'  # Nombres completos (dos palabras con mayúsculas)
    
    # Extracciones usando las regex
    serials = re.findall(serial_pattern, row_text)
    emails = re.findall(email_pattern, row_text)
    phones = re.findall(phone_pattern, row_text)
    dates = re.findall(date_pattern, row_text)
    values = re.findall(value_pattern, row_text)
    names = re.findall(name_pattern, row_text)
    
    # Separamos los contactos por comas (si hay varios)
    contacts = ', '.join(emails + phones + names[1:]) if emails or phones or names[1:] else None
    contacts_list = contacts.split(', ') if contacts else []

    # Asignamos cada tipo de contacto a una columna
    contact_columns = {
        'Email': contacts_list[0] if len(contacts_list) > 0 else None,
        'Telefono': contacts_list[1] if len(contacts_list) > 1 else None,
        'Nombre adicional': contacts_list[2] if len(contacts_list) > 2 else None,
    }
    
    # Tomar el primero de cada tipo, si existe
    return {
        'Número de serie': serials[0] if serials else None,
        'Nombre del producto': names[0] if names else None,
        'Valor': values[0] if values else None,
        'Fecha de compra': dates[0] if dates else None,
        **contact_columns  # Desempaqueta las columnas de contacto en el diccionario de resultados
    }

# Configuración de la app
st.title("Procesamiento de Productos con Regex por Lehvui Gonzalez")

url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/main/archivos-datos/regex/regex_productos.csv"

# Leer el archivo subido
response = requests.get(url)
response.raise_for_status()
data = pd.read_csv(io.StringIO(response.text))
    
# Procesar los datos
processed_data = data.apply(extract_info, axis=1, result_type='expand')
    
st.write("Datos procesados:")
st.dataframe(processed_data)
    
# Generar archivo Excel en memoria
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    processed_data.to_excel(writer, index=False, sheet_name='Productos')
    
# Botón para descargar el archivo
st.download_button(
    label="Descargar archivo Excel",
    data=output.getvalue(),
    file_name="productos_procesados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

