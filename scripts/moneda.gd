extends Area2D
## Moneda recogible: avisa con la señal "recogida" y desaparece (niveles 5 y 6).

signal recogida(posicion: Vector2)


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	if body is CharacterBody2D:
		recogida.emit(global_position)
		queue_free()
