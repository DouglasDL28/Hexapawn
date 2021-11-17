from os import read
import numpy as np


from HexapawnMTC import HexapawnMTC


menu = [
    "Mover ficha",
    "Enseñar tablero",
    "Salir"
]

actions_menu = [
    "Seleccionar movimiento",
    "Ver movimiento",
    "regresar"
]


def int_input(text):
    while True:
        i = input(text)
        try:
            return int(i)
        except:
            print("Ingrese un valor númerico")


def get_index_option(list_item, text="Selecciona una opcion:\n"):
    while True:
        for index, i in enumerate(list_item):
            print(str(index + 1), ") ", str(i))
        selected = int_input(text)
        size = len(list_item)
        if selected > 0 and selected <= size:
            return selected - 1
        else:
            print("Seleccione un número valido")


if __name__ == "__main__":
    game = HexapawnMTC(state=[
        [(0, 0), (1, 0), (2, 0)],
        [(0, 2), (1, 2), (2, 2)]
    ])

    game_running = True
    while game_running:
        selected_option = get_index_option(menu)
        if selected_option == 0:
            # Game
            action_option = 0
            while action_option != 2:
                action_option = get_index_option(actions_menu)
                if action_option == 0:
                    # Seleccionamos movimiento
                    action_selected = game.select_legal_action()
                    game.state = game.move(action_selected)
                    if game.is_terminal_node():
                        game.print_winner()
                        game_running = False
                        break
                    print("ANTES DE SIMULAR")
                    game.print_board()
                    simulation = HexapawnMTC(
                        state=[i.copy() for i in game.state.copy()],
                        player_one=False
                    )
                    # Simular turno del oponente
                    # Jalamos nuestra mejor acción
                    won = simulation.best_action()

                    # Toggle turn
                    game.player_one = False

                    game.state = game.move(won.parent_action)
                    game.player_one = True

                    print("DESPUES DE SIMULAR")
                    game.print_board()
                    if game.is_terminal_node():
                        game.print_winner()
                        game_running = False
                        break
                    action_option = 2
                # Imprimimos acciones
                elif action_option == 1:
                    game.print_actions()
        # Imprimimos el board
        elif selected_option == 1:
            game.print_board()
        else:
            game_running = False
            print("Gracias por jugar")
