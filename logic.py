"""Plantilla con las funciones que el alumnado debe completar para M3.

La capa gráfica llama a estas funciones para mover el estado del juego. No es
necesario crear clases; basta con manipular listas, diccionarios y tuplas.
"""
from __future__ import annotations

import random
from typing import Dict, List, Tuple

STATE_HIDDEN = "hidden"
STATE_VISIBLE = "visible"
STATE_FOUND = "found"

Card = Dict[str, str]
Board = List[List[Card]]
Position = Tuple[int, int]
GameState = Dict[str, object]


def build_symbol_pool(rows: int, cols: int) -> List[str]:
    """Crea la lista de símbolos necesaria para rellenar todo el tablero. """
    
    num_pairs = (rows * cols) // 2
    
    # Fuente de símbolos (letras, números y caracteres especiales)
    available_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&?+*"
    
    # Aseguro tener suficientes símbolos repitiendo la cadena si el tablero es muy grande
    while len(available_chars) < num_pairs:
        available_chars += available_chars
        
    # Selecciono solo los necesarios y los duplicamos
    selected_symbols = list(available_chars[:num_pairs])
    deck = selected_symbols * 2
    
    # Barajo la lista
    random.shuffle(deck)
    
    return deck


def create_game(rows: int, cols: int) -> GameState:
    """Genera el diccionario con el estado inicial del juego."""

    deck = build_symbol_pool(rows, cols)
    board = []

    # Construyo el tablero fila a fila
    for _ in range(rows):
        row_list = []
        for _ in range(cols):
            # Saco una carta de la baraja mezclada
            symbol = deck.pop()
            card = {
                "symbol": symbol,
                "state": STATE_HIDDEN
            }
            row_list.append(card)
        board.append(row_list)

    return {
        "board": board,
        "pending": [],      # Lista de coordenadas [(fil, col)] de cartas volteadas
        "moves": 0,         # Contador de turnos
        "matches": 0,       # Contador de parejas encontradas
        "total_pairs": (rows * cols) // 2,
        "rows": rows,
        "cols": cols
    }
    



def reveal_card(game: GameState, row: int, col: int) -> bool:
    """Intenta descubrir la carta ubicada en ``row``, ``col``."""

    board = game["board"]
    pending = game["pending"]

    # Valido coordenadas 
    if not (0 <= row < game["rows"] and 0 <= col < game["cols"]):
        return False

    card = board[row][col]

    # Si la carta ya está visible o encontrada, no hago nada
    if card["state"] != STATE_HIDDEN:
        return False

    # Si ya hay 2 cartas levantadas esperando resolución, no permito levantar una tercera
    if len(pending) >= 2:
        return False

    # Revelo la carta y la añado a pendientes
    card["state"] = STATE_VISIBLE
    pending.append((row, col))

    return True


def resolve_pending(game: GameState) -> Tuple[bool, bool]:
    """Resuelve el turno si hay dos cartas pendientes."""

    pending = game["pending"]
    board = game["board"]

    # Si no hay 2 cartas pendientes, no hay nada que resolver
    if len(pending) != 2:
        return False, False

    # Recupero las coordenadas y las cartas
    pos1 = pending[0]
    pos2 = pending[1]
    card1 = board[pos1[0]][pos1[1]]
    card2 = board[pos2[0]][pos2[1]]

    match_found = False

    # Comparo símbolos
    if card1["symbol"] == card2["symbol"]:
        # ¡Son pareja!
        card1["state"] = STATE_FOUND
        card2["state"] = STATE_FOUND
        game["matches"] += 1
        match_found = True
    else:
        # No coinciden, las vuelvo a ocultar
        card1["state"] = STATE_HIDDEN
        card2["state"] = STATE_HIDDEN

    # En ambos casos, el turno termina por lo que aumento movimientos y limpio pendientes
    game["moves"] += 1
    game["pending"] = [] # Vacio la lista para el siguiente turno

    # Devuelvo (True porque se resolvió, y si hubo match o no)
    return True, match_found


def has_won(game: GameState) -> bool:
    """Indica si se han encontrado todas las parejas."""

    return game["matches"] == game["total_pairs"]
