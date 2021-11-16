""" Hexapawn implementation with MCTS. """

import numpy as np

from Node import Node

class Hexapawn(object):
    """ Hexapawn game class. Contains game state and methods. """

    def __init__(self, init_state: np.ndarray):
        self.player_one_turn = True
        self.board = self.get_state_board(init_state)
        self.moves_count = 0

        self.curr_node = Node(
            state=init_state,
            parent=None,
            action=None
        )

    def get_state_board(self, state: np.ndarray):
        board = np.array([
                [0, 0, 0,],
                [0, 0, 0,],
                [0, 0, 0,],
            ],
            dtype=np.uint8
        )

        # Player 1
        for pair in state[0]:
            board[pair[1]][pair[0]] = 1

        # Player 2
        for pair in state[1]:
            board[pair[1]][pair[0]] = 2
    
        return board

    def result(self, node:Node, action:np.ndarray, player_one):
        player = 0 if player_one else 1
        new_state = np.copy(node.state)

        # TODO: mostrar resultado de la acción en estado
        # implica eliminar piezas cuando sea necesario

        new_node = Node(
            state=new_state,
            parent=node,
            action=action,
        )

        return new_node

    def actions(self, node:Node, player_one:bool):
        """ Gets player actions in a given state. """

        actions = []

        player = 0 if player_one else 1
        delta_y = 1 if player_one else -1

        board = self.get_state_board(node.state)

        for piece in node.state[player]:
            p_x, p_y = piece[0], piece[1]

            if self.in_board(p_x, p_y+delta_y) and board[p_y+delta_y][p_x]==0:
                # vertical move
                actions.append((p_x, p_y+delta_y))

            for opp_piece in node.state[(player + 1) % 2]:
                opp_x, opp_y = opp_piece[0], opp_piece[1]

                if opp_x==p_x+1 or opp_x==p_x-1:
                    if opp_y==p_y+delta_y:
                        # can eat a piece
                        actions.append((opp_x, opp_y))
                
                            
        return actions

    def move(self, coord:np.ndarray, dest_coord:np.ndarray):
        return
    
    
    def check_direction(self, coord:np.ndarray, node:Node, delta_x:int, delta_y:int, valid_dests:list=[]):
        return

    def in_board(self, X:int, Y:int):
        if X<=2 and X>=0 and Y<=2 and Y>=0:
            return True
        
        return False

    def is_terminal(self, node:Node):
        """ Check if game ends. """

        return

    def MCTS(self, state):
        """ Monte Carlo Tree Search. """
        # returns an action.
        pass