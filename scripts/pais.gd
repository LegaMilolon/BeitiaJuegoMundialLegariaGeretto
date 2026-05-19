extends Area2D

var nom = ""


func _on_mouse_entered():
	for hijo in get_children():
		if hijo is Polygon2D:
			hijo.modulate = Color(1.0, 0.95, 0.3, 0.45)


func _on_mouse_exited():
	for hijo in get_children():
		if hijo is Polygon2D:
			hijo.modulate = Color(1.0, 1.0, 1.0, 0.0)
