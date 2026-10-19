extends Node2D
## Escena jugable que reúne los niveles 2 a 7:
## personaje animado, nivel con TileMapLayer, partículas, música y efectos por buses,
## interfaz con diálogo. La tecla C abre el cofre 3D (nivel 4).

const INICIO := Vector2(64, 280)
const LIMITE_CAIDA := 440.0
const ESCENA_COFRE := "res://escenas/cofre_3d.tscn"

var monedas: int = 0
var en_dialogo: bool = false

# Sin tipo estático: estos nodos tienen scripts propios con métodos y señales.
@onready var jugador = $Jugador
@onready var efectos = $Efectos
@onready var interfaz = $Interfaz
@onready var guardian = $Guardian
@onready var musica: AudioStreamPlayer = $Musica
@onready var sfx_salto: AudioStreamPlayer = $SfxSalto
@onready var sfx_recoger: AudioStreamPlayer = $SfxRecoger
@onready var sfx_dano: AudioStreamPlayer = $SfxDano


func _ready() -> void:
	# Bucle de la música (equivale a activar Loop en la pestaña Import del .ogg).
	if musica.stream is AudioStreamOggVorbis:
		(musica.stream as AudioStreamOggVorbis).loop = true
	musica.play()

	jugador.salto.connect(sfx_salto.play)
	for moneda in $Monedas.get_children():
		moneda.recogida.connect(_on_moneda_recogida)
	guardian.dialogo_solicitado.connect(_on_dialogo_solicitado)
	interfaz.dialogo_terminado.connect(_on_dialogo_terminado)
	interfaz.actualizar_monedas(monedas)


func _physics_process(_delta: float) -> void:
	if jugador.global_position.y > LIMITE_CAIDA:
		_caer()


func _unhandled_input(event: InputEvent) -> void:
	var tecla := event as InputEventKey
	if tecla and tecla.pressed and not tecla.echo and tecla.keycode == KEY_C and not en_dialogo:
		get_tree().change_scene_to_file(ESCENA_COFRE)


func _caer() -> void:
	sfx_dano.play()
	efectos.disparar(jugador.global_position - Vector2(0, 40))
	jugador.global_position = INICIO
	jugador.velocity = Vector2.ZERO
	jugador.get_node("Camera2D").reset_smoothing()


func _on_moneda_recogida(posicion: Vector2) -> void:
	monedas += 1
	sfx_recoger.play()
	efectos.disparar(posicion)
	interfaz.actualizar_monedas(monedas)


func _on_dialogo_solicitado(ruta: String, titulo: String) -> void:
	en_dialogo = true
	jugador.congelar(true)
	interfaz.mostrar_dialogo(ruta, titulo)


func _on_dialogo_terminado() -> void:
	await get_tree().create_timer(0.2).timeout
	en_dialogo = false
	jugador.congelar(false)
