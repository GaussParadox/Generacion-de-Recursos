extends CharacterBody2D
## Jugador 2D (niveles 2 y 3).
## Requiere un hijo AnimatedSprite2D con las animaciones "quieto" y "caminar".
## Controles: flechas izquierda/derecha para moverse, espacio, Enter o flecha arriba para saltar.

signal salto

@export var velocidad: float = 140.0
@export var fuerza_salto: float = -400.0

var gravedad: float = ProjectSettings.get_setting("physics/2d/default_gravity")

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D


func congelar(valor: bool) -> void:
	set_physics_process(not valor)
	if valor:
		velocity = Vector2.ZERO
		sprite.play("quieto")


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y += gravedad * delta

	var quiere_saltar := Input.is_action_just_pressed("ui_accept") or Input.is_action_just_pressed("ui_up")
	if quiere_saltar and is_on_floor():
		velocity.y = fuerza_salto
		salto.emit()

	var direccion := Input.get_axis("ui_left", "ui_right")
	velocity.x = direccion * velocidad

	if direccion != 0.0:
		sprite.flip_h = direccion < 0.0
		sprite.play("caminar")
	else:
		sprite.play("quieto")

	move_and_slide()
