extends Node2D
## Pinta el nivel a partir de mapas de texto (nivel 3).
## Suelo: G=pasto  D=tierra  B=ladrillo  M=ladrillo con musgo  P=plataforma (un solo sentido)
## Decoración: b=arbusto  m=hongo  v=enredadera
## Cada letra es una baldosa del atlas assets/tiles/tileset_bosque.png.
## Para repintar a mano, comente la llamada a _pintar en _ready y use el panel TileMap.

const SUELO: Array = [
	"B..............................................B",
	"B..............................................B",
	"B..............................................B",
	"B..............................................B",
	"B..............................................B",
	"B..............................................B",
	"B....................PPPP......................B",
	"B.......PPP..........................M.........B",
	"B.................MM................MM.........B",
	"GGGGGGGGGGGGG..GGGGGGGGGGGGGG..GGGGGGGGGGGGGGGGG",
	"DDDDDDDDDDDDD..DDDDDDDDDDDDDD..DDDDDDDDDDDDDDDDD",
	"DDDDDDDDDDDDD..DDDDDDDDDDDDDD..DDDDDDDDDDDDDDDDD"
]

const DECORACION: Array = [
	"................................................",
	"................................................",
	"................................................",
	"................................................",
	"................................................",
	"................................................",
	"................................................",
	".....................v..v.......................",
	"....b.m.v.v..............b.m.....b.....m.b......",
	"................................................",
	"................................................",
	"................................................"
]

const TILES_SUELO := {
	"G": Vector2i(0, 0),
	"D": Vector2i(1, 0),
	"B": Vector2i(2, 0),
	"M": Vector2i(3, 0),
	"P": Vector2i(0, 1),
}

const TILES_DECORACION := {
	"b": Vector2i(1, 1),
	"m": Vector2i(2, 1),
	"v": Vector2i(3, 1),
}

@onready var capa_suelo: TileMapLayer = $Suelo
@onready var capa_decoracion: TileMapLayer = $Decoracion


func _ready() -> void:
	_pintar(SUELO, TILES_SUELO, capa_suelo)
	_pintar(DECORACION, TILES_DECORACION, capa_decoracion)


func _pintar(mapa: Array, tiles: Dictionary, capa: TileMapLayer) -> void:
	for y in mapa.size():
		var fila: String = mapa[y]
		for x in fila.length():
			var letra: String = fila[x]
			if tiles.has(letra):
				capa.set_cell(Vector2i(x, y), 0, tiles[letra])
