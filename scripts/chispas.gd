extends Node2D
## Efecto de partículas de un solo disparo (nivel 5).
## Requiere un hijo GPUParticles2D llamado "Chispas" (One Shot activado).


func disparar(posicion: Vector2) -> void:
	$Chispas.global_position = posicion
	$Chispas.restart()
