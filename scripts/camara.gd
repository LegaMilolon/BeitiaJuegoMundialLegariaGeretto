extends Camera2D

var direccion_zm: float = 0.0
@export var velocidad_zm: float = 2.0
@export var zm_max: float = 8.0
@export var zm_min: float = 1.0

@export var velocidad_mov: float = 400.0
@export var margen_pan: int = 16

var arrastrndo = false
var pos_maus_vieja = Vector2.ZERO
var ancho_mapa = 1920
var alto_mapa = 1080


func _ready():
	position = Vector2(ancho_mapa /2.0, alto_mapa /2.0)
	await get_tree().process_frame
	var tam = get_window().size
	var zm_x = float(tam.x) /float(ancho_mapa)
	var zm_y = float(tam.y) /float(alto_mapa)
	zm_min = min(zm_x, zm_y)
	zoom = Vector2(zm_min, zm_min)


func _process(delta):
	_hacer_zoom(delta)
	_mover_teclado(delta)
	_pan_bordes(delta)
	_limitar_posicion()


func _unhandled_input(ev):
	if ev.is_action("camara_acercar"):
		direccion_zm = 1
	elif ev.is_action("camara_alejar"):
		direccion_zm = -1
	if ev is InputEventMouseButton:
		if ev.button_index == MOUSE_BUTTON_RIGHT:
			arrastrndo =ev.pressed
			pos_maus_vieja =ev.position
	if ev is InputEventMouseMotion:
		if arrastrndo:
			var dif = ev.position -pos_maus_vieja
			position -= dif /zoom
			pos_maus_vieja =ev.position


func _hacer_zoom(delta):
	var nuevo_zm = clamp(zoom.x +(velocidad_zm *zoom.x) *direccion_zm *delta, zm_min, zm_max)
	zoom = Vector2(nuevo_zm, nuevo_zm)
	direccion_zm *= 0.85


func _mover_teclado(delta):
	var dir = Vector2.ZERO
	if Input.is_action_pressed("camara_arriba"): dir.y -= 1
	if Input.is_action_pressed("camara_abajo"): dir.y += 1
	if Input.is_action_pressed("camara_izquierda"): dir.x -= 1
	if Input.is_action_pressed("camara_derecha"): dir.x += 1
	position += dir.normalized() *(velocidad_mov /zoom.x) *delta


func _pan_bordes(delta):
	var vp = get_viewport()
	var tam_vp = vp.get_visible_rect().size
	var maus = vp.get_mouse_position()
	var dir_pan = Vector2(-1, -1)
	if maus.x <margen_pan or maus.x >tam_vp.x -margen_pan:
		if maus.x >tam_vp.x /2.0:
			dir_pan.x = 1
		position.x += dir_pan.x *(velocidad_mov /zoom.x) *delta
	if maus.y <margen_pan or maus.y >tam_vp.y -margen_pan:
		if maus.y >tam_vp.y /2.0:
			dir_pan.y = 1
		position.y += dir_pan.y *(velocidad_mov /zoom.x) *delta


func _limitar_posicion():
	var tam = get_window().size
	var mitad_vp_w = (float(tam.x) /2.0) /zoom.x
	var mitad_vp_h = (float(tam.y) /2.0) /zoom.y
	var lim_izq = mitad_vp_w
	var lim_der = ancho_mapa -mitad_vp_w
	var lim_arr = mitad_vp_h
	var lim_abj = alto_mapa -mitad_vp_h
	if lim_izq >lim_der:
		position.x = ancho_mapa /2.0
	else:
		position.x = clamp(position.x, lim_izq, lim_der)
	if lim_arr >lim_abj:
		position.y = alto_mapa /2.0
	else:
		position.y = clamp(position.y, lim_arr, lim_abj)
