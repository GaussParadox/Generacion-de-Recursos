extends Area2D
## Personaje no jugador que abre un diálogo al acercarse (nivel 7).
## Emite dialogo_solicitado con la ruta del archivo .dialogue y el título inicial.
## El archivo usa la sintaxis de Dialogue Manager (ver escenas/dialogos/guardian.dialogue).

signal dialogo_solicitado(ruta: String, titulo: String)

@export_file("*.dialogue") var archivo_dialogo: String = "res://escenas/dialogos/guardian.dialogue"
@export var titulo_inicial: String = "inicio"

var _dentro: bool = false


func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)


func _on_body_entered(body: Node2D) -> void:
	if _dentro or not body is CharacterBody2D:
		return
	_dentro = true
	dialogo_solicitado.emit(archivo_dialogo, titulo_inicial)


func _on_body_exited(body: Node2D) -> void:
	if body is CharacterBody2D:
		_dentro = false
