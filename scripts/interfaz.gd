extends CanvasLayer
## Interfaz del juego (nivel 7): contador de monedas y caja de diálogo.
##
## El diálogo se lee del archivo .dialogue con la sintaxis de Dialogue Manager:
##   ~ titulo            inicia un bloque
##   Nombre: texto       línea de diálogo
##   - opción => titulo  respuesta que salta a otro bloque
##   => titulo / => END  salto al terminar el bloque
## Así el juego funciona sin el addon; con Dialogue Manager instalado puede usar
## DialogueManager.show_dialogue_balloon() con el mismo archivo.

signal dialogo_terminado

var bloques: Dictionary = {}
var _lineas: Array = []
var _indice: int = 0
var _bloque_actual: Dictionary = {}
var _activo: bool = false

@onready var panel: NinePatchRect = $Dialogo
@onready var texto: Label = $Dialogo/Texto
@onready var opciones: VBoxContainer = $Dialogo/Opciones
@onready var etiqueta_monedas: Label = $HUD/Monedas


func _ready() -> void:
	panel.visible = false


func actualizar_monedas(cantidad: int) -> void:
	etiqueta_monedas.text = "Monedas: %d" % cantidad


func mostrar_dialogo(ruta: String, titulo: String) -> void:
	_cargar(ruta)
	if not bloques.has(titulo):
		push_error("No existe el título de diálogo: " + titulo)
		dialogo_terminado.emit()
		return
	_activo = true
	panel.visible = true
	_ir_a(titulo)


func _cargar(ruta: String) -> void:
	bloques.clear()
	var archivo := FileAccess.open(ruta, FileAccess.READ)
	if archivo == null:
		push_error("No se pudo abrir " + ruta)
		return
	var actual: String = ""
	while not archivo.eof_reached():
		var linea: String = archivo.get_line().strip_edges()
		if linea == "" or linea.begins_with("#"):
			continue
		if linea.begins_with("~ "):
			actual = linea.substr(2).strip_edges()
			bloques[actual] = {"lineas": [], "opciones": [], "siguiente": "END"}
		elif actual == "":
			continue
		elif linea.begins_with("- "):
			var partes: PackedStringArray = linea.substr(2).split("=>")
			var destino: String = "END"
			if partes.size() > 1:
				destino = partes[1].strip_edges()
			bloques[actual]["opciones"].append({"texto": partes[0].strip_edges(), "destino": destino})
		elif linea.begins_with("=>"):
			bloques[actual]["siguiente"] = linea.substr(2).strip_edges()
		else:
			bloques[actual]["lineas"].append(linea)


func _ir_a(titulo: String) -> void:
	if titulo == "END" or not bloques.has(titulo):
		_terminar()
		return
	_bloque_actual = bloques[titulo]
	_lineas = _bloque_actual["lineas"]
	_indice = 0
	_mostrar_linea()


func _mostrar_linea() -> void:
	_limpiar_opciones()
	var hay_opciones: bool = not _bloque_actual["opciones"].is_empty()
	if _lineas.is_empty():
		if hay_opciones:
			texto.text = ""
			_crear_opciones()
		else:
			_ir_a(_bloque_actual["siguiente"])
		return
	if _indice >= _lineas.size():
		_ir_a(_bloque_actual["siguiente"])
		return
	texto.text = _lineas[_indice]
	if _indice == _lineas.size() - 1 and hay_opciones:
		_crear_opciones()


func _crear_opciones() -> void:
	for opcion in _bloque_actual["opciones"]:
		var boton := Button.new()
		boton.text = opcion["texto"]
		boton.pressed.connect(_ir_a.bind(opcion["destino"]))
		opciones.add_child(boton)
	opciones.get_child(0).grab_focus()


func _limpiar_opciones() -> void:
	for hijo in opciones.get_children():
		opciones.remove_child(hijo)
		hijo.queue_free()


func _unhandled_input(event: InputEvent) -> void:
	if not _activo:
		return
	if event.is_action_pressed("ui_accept"):
		get_viewport().set_input_as_handled()
		if opciones.get_child_count() == 0:
			_indice += 1
			_mostrar_linea()


func _terminar() -> void:
	_activo = false
	panel.visible = false
	_limpiar_opciones()
	dialogo_terminado.emit()
