# Este script descarga el GeoJSON completo de Natural Earth y lo guarda tal cual en datos/paises.json.
# No procesa ni simplifica nada, el archivo conserva todos los metadatos originales de cada pais.
# Hay que ejecutarlo UNA vez antes de abrir el proyecto, o si se quiere actualizar los datos.
# No requiere librerias externas, solo Python 3 estandar.

import urllib.request
import json
import os

# URL del GeoJSON de Natural Earth con las fronteras de todos los paises a escala 1:110m.
# Contiene geometria, nombre, codigo ISO, poblacion, continente y muchos otros metadatos.
URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"

print("descargando datos del mapa...")
respuesta = urllib.request.urlopen(URL)
# Leemos el contenido crudo como texto y lo parseamos a un dict de Python.
datos_geo = json.loads(respuesta.read().decode("utf-8"))
print(f"descarga completa, {len(datos_geo['features'])} paises encontrados")

# Construye la ruta de salida relativa a la raiz del proyecto (carpeta datos/).
ruta_salida = os.path.join(os.path.dirname(__file__), "..", "datos", "paises.json")
ruta_salida = os.path.normpath(ruta_salida)
os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

# Guardamos el GeoJSON completo sin modificarlo.
# ensure_ascii=False para que los nombres con tildes se guarden correctamente.
with open(ruta_salida, "w", encoding="utf-8") as f:
	json.dump(datos_geo, f, ensure_ascii=False)

print(f"listo! GeoJSON completo guardado en {ruta_salida}")
