extends Node3D
## Visor del cofre 3D con material PBR (nivel 4).
## Aplica madera.tres (albedo + normal + roughness) como Material Override del .glb.
## Esc o C vuelven a la escena principal.

const MATERIAL: Material = preload("res://assets/texturas/madera.tres")

@onready var modelo: Node3D = $Modelo
@onready var luz: DirectionalLight3D = $DirectionalLight3D


func _ready() -> void:
	luz.rotation_degrees = Vector3(-50.0, -30.0, 0.0)
	var mallas: Array = modelo.find_children("*", "MeshInstance3D", true, false)
	if modelo is MeshInstance3D:
		mallas.append(modelo)
	for malla in mallas:
		malla.material_override = MATERIAL


func _process(delta: float) -> void:
	modelo.rotate_y(delta * 0.6)


func _unhandled_input(event: InputEvent) -> void:
	var tecla := event as InputEventKey
	var volver := event.is_action_pressed("ui_cancel")
	if tecla and tecla.pressed and not tecla.echo and tecla.keycode == KEY_C:
		volver = true
	if volver:
		get_tree().change_scene_to_file("res://escenas/main.tscn")
