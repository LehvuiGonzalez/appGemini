import requests
import pandas as pd

def leer_csv_desde_url(url):
  """Lee un archivo CSV directamente desde una URL.

  Args:
    url (str): La URL del archivo CSV.

  Returns:
    pandas.DataFrame: Un DataFrame de pandas con los datos del CSV.
  """

  response = requests.get(url)
  response.raise_for_status()  # Levanta una excepción si la solicitud falla

  # Crear un DataFrame directamente desde el contenido de la respuesta
  df = pd.read_csv(io.StringIO(response.text))
  return df

# Ejemplo de uso:
url_archivo = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/main/archivos-datos/regex/regex_productos.csv"
df = leer_csv_desde_url(url_archivo)

print(df)
