extends Node2D

var ruta_datos = "res://datos/paises.json"
var paises_lista = []
var ANCHO = 1920.0
var ALTO = 1080.0


func _ready():
	var tam = get_viewport().get_visible_rect().size
	var escala_x = tam.x / ANCHO
	var escala_y = tam.y / ALTO

	var fondo = $MapaFondo
	fondo.position = tam / 2.0
	fondo.scale = Vector2(escala_x, escala_y)

	scale = Vector2(escala_x, escala_y)

	cargar_todo()


func lon_a_x(lon):
	return (lon + 180.0) / 360.0 * ANCHO

func lat_a_y(lat):
	return (90.0 - lat) / 180.0 * ALTO


func poligono_mas_grande(lista):
	var mejor = lista[0]
	for p in lista:
		if p.size() > mejor.size():
			mejor = p
	return mejor


func cargar_todo():
	var f = FileAccess.open(ruta_datos, FileAccess.READ)
	if f == null:
		printerr("no se pudo abrir paises.json")
		return
	var txt = f.get_as_text()
	f.close()
	var geo = JSON.parse_string(txt)
	if geo == null:
		printerr("error al parsear paises.json")
		return
	for feat in geo["features"]:
		var geom = feat["geometry"]
		if geom == null:
			continue
		var nombre = feat["properties"].get("NAME", "desconocido")
		var tipo = geom["type"]
		var lista_poligs = []
		if tipo == "Polygon":
			lista_poligs = [geom["coordinates"][0]]
		elif tipo == "MultiPolygon":
			for parte in geom["coordinates"]:
				lista_poligs.append(parte[0])
		else:
			continue
		var anillo = poligono_mas_grande(lista_poligs)
		_crear_pais(nombre, anillo)
	print("paises cargados: ", paises_lista.size())


func _crear_pais(nombre, coordenadas):
	var pts = PackedVector2Array()
	for coord in coordenadas:
		pts.append(Vector2(lon_a_x(coord[0]), lat_a_y(coord[1])))

	var nodo_pais = Area2D.new()
	nodo_pais.set_script(load("res://scripts/pais.gd"))
	nodo_pais.nom = nombre
	nodo_pais.name = nombre
	add_child(nodo_pais)

	var poligono = Polygon2D.new()
	poligono.polygon = pts
	poligono.modulate = Color(1.0, 1.0, 1.0, 0.0)
	nodo_pais.add_child(poligono)

	var colision = CollisionPolygon2D.new()
	colision.polygon = pts
	nodo_pais.add_child(colision)

	var linea = Line2D.new()
	linea.points = pts
	linea.closed = true
	linea.width = 0.5
	linea.modulate = Color(0.0, 0.0, 0.0, 0.5)
	nodo_pais.add_child(linea)

	nodo_pais.mouse_entered.connect(nodo_pais._on_mouse_entered)
	nodo_pais.mouse_exited.connect(nodo_pais._on_mouse_exited)

	paises_lista.append(nodo_pais)
