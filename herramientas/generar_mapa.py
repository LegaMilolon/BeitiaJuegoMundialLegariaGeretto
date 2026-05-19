# Este script genera la imagen del mapa mundial (mapa_mundo.png) que se usa como fondo en el juego.
# Descarga los datos geograficos de Natural Earth (GeoJSON con fronteras reales de cada pais),
# los proyecta a pixeles y los dibuja sobre un lienzo de 1920x1080.
# Hay que ejecutarlo UNA vez antes de abrir el proyecto en Godot, o cada vez que se quiera regenerar el mapa.
# Requiere Python 3 y la libreria Pillow (se instala sola si no esta).

import json
import os
import urllib.request
import random

# Intentamos importar Pillow. Si no esta instalada, la instalamos automaticamente.
try:
	from PIL import Image, ImageDraw
except ImportError:
	import subprocess, sys
	subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
	from PIL import Image, ImageDraw

# Resolucion final de la imagen generada. Tiene que coincidir con la resolucion del proyecto Godot.
ANCHO = 1920
ALTO = 1080

# URL del archivo GeoJSON de Natural Earth a 110m de resolucion.
# Contiene los poligonos de todos los paises del mundo con fronteras reales simplificadas.
URL_GEO = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"

# Paleta de verdes naturales para los paises. Se aplica en ciclo para que paises vecinos
# tengan tonos distintos y se distingan entre si visualmente.
PALETA =[
	(111, 150, 90),
	(120, 160, 85),
	(100, 140, 75),
	(130, 165, 95),
	(95, 135, 70),
	(115, 155, 88),
	(105, 145, 80),
	(125, 158, 92),
]

# Color del oceano / fondo del lienzo (azul oscuro).
COLOR_MAR =(40, 80, 140)
# Color de las lineas de frontera entre paises (casi negro).
COLOR_BORDE =(20, 20, 20)
# Color real que se usa para el fondo (el COLOR_MAR no se usa directamente, este si).
COLOR_FONDO =(38, 77, 135)


# Convierte una longitud geografica (-180 a 180) a un pixel X en la imagen.
# Usa proyeccion equirectangular: reparte los 360 grados de longitud en el ancho de la imagen.
def lon_a_x(lon):
	return (lon +180) / 360 * ANCHO

# Convierte una latitud geografica (90 a -90) a un pixel Y en la imagen.
# Y=0 es arriba (polo norte), Y=ALTO es abajo (polo sur).
def lat_a_y(lat):
	return (90 -lat) / 180 * ALTO


# Toma una lista de coordenadas [longitud, latitud] del GeoJSON
# y las convierte a una lista de tuplas (x, y) en pixeles para Pillow.
def coords_a_puntos(ring):
	pts = []
	for c in ring:
		x = lon_a_x(c[0])
		y = lat_a_y(c[1])
		pts.append((x, y))
	return pts


respuesta = urllib.request.urlopen(URL_GEO)
geo = json.loads(respuesta.read().decode("utf-8"))

# Creamos el lienzo en blanco con el color del oceano como fondo.
img = Image.new("RGB", (ANCHO, ALTO), COLOR_FONDO)
draw = ImageDraw.Draw(img)

# --- PRIMER PASADA: dibujar los rellenos de cada pais ---
# Recorremos todos los "features" del GeoJSON (cada feature es un pais).
idx = 0
for feat in geo["features"]:
	geom = feat["geometry"]
	if geom is None:
		continue
	# Asignamos un color de la paleta rotando por indice.
	color = PALETA[idx % len(PALETA)]
	idx +=1
	tipo = geom["type"]
	# Un pais puede ser un Polygon simple (isla o territorio continuo)
	# o un MultiPolygon (pais con varias partes, como Indonesia o EEUU con Alaska).
	if tipo == "Polygon":
		poligonos = [geom["coordinates"]]
	elif tipo == "MultiPolygon":
		poligonos = geom["coordinates"]
	else:
		continue
	for parte in poligonos:
		# El primer anillo de cada parte es el contorno exterior del territorio.
		# Los anillos siguientes serian huecos (lagos, etc.) que ignoramos por simplicidad.
		anillo = parte[0]
		pts = coords_a_puntos(anillo)
		if len(pts) >= 3:
			draw.polygon(pts, fill=color)

# --- SEGUNDA PASADA: dibujar las fronteras encima de los rellenos ---
# Se hace en una segunda vuelta para que las lineas queden siempre visibles
# y no queden tapadas por el relleno del pais de al lado.
for feat in geo["features"]:
	geom = feat["geometry"]
	if geom is None:
		continue
	tipo = geom["type"]
	if tipo == "Polygon":
		poligonos = [geom["coordinates"]]
	elif tipo == "MultiPolygon":
		poligonos = geom["coordinates"]
	else:
		continue
	for parte in poligonos:
		anillo = parte[0]
		pts = coords_a_puntos(anillo)
		if len(pts) >= 2:
			# Cerramos el poligono agregando el primer punto al final de la linea.
			draw.line(pts +[pts[0]], fill=COLOR_BORDE, width=1)

# Guardamos la imagen en sprites/mapa_mundo.png relativo a la raiz del proyecto.
ruta = os.path.join(os.path.dirname(__file__), "..", "sprites", "mapa_mundo.png")
ruta = os.path.normpath(ruta)
os.makedirs(os.path.dirname(ruta), exist_ok=True)
img.save(ruta)
