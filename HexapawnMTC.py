import numpy as np
from collections import defaultdict


def any_lambda(iterable, function):
    return any(function(i) for i in iterable)


class HexapawnMTC():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self.player_one = True
        return

    def win_lose_difference(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def number_of_visits(self):
        return self._number_of_visits

    def untried_actions(self):

        self._untried_actions = self.get_legal_actions()
        return self._untried_actions

    def expand(self):

        action = self._untried_actions.pop()
        next_state = self.move(action)
        child_node = HexapawnMTC(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def rollout(self):
        current_rollout_state = self

        while not current_rollout_state.is_terminal_node():

            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def best_child(self, c_param=0.1):
        choices_weights = [(c.win_lose_difference() / c.number_of_visits()) + c_param *
                           np.sqrt((2 * np.log(self.number_of_visits()) / c.number_of_visits())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):

        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):

            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)

    def get_legal_actions(self):
        """ Gets player actions in a given state. """

        actions = []

        player = 0 if self.player_one else 1
        delta_y = 1 if self.player_one else -1

        board = self.get_state_board(self.state)

        for piece in self.state[player]:
            p_x, p_y = piece[0], piece[1]

            if self.in_board(p_x, p_y+delta_y) and board[p_y+delta_y][p_x] == 0:
                # vertical move
                # We also add the origin position
                actions.append([(p_x, p_y), (p_x, p_y+delta_y)])

            for opp_piece in self.state[(player + 1) % 2]:
                opp_x, opp_y = opp_piece[0], opp_piece[1]

                if opp_x == p_x+1 or opp_x == p_x-1:
                    if opp_y == p_y+delta_y:
                        # can eat a piece
                        actions.append([(p_x, p_y), (opp_x, opp_y)])

        return actions

    def get_state_board(self, state: np.ndarray):
        board = np.array([
            [0, 0, 0, ],
            [0, 0, 0, ],
            [0, 0, 0, ],
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

    def in_board(self, X: int, Y: int):
        if X <= 2 and X >= 0 and Y <= 2 and Y >= 0:
            return True

        return False

    def is_terminal_node(self):
        board = self.get_state_board(self.state)
        first_row = board[0]
        last_row = board[2]
        second_won = any_lambda(first_row, lambda x: x == 2)
        first_won = any_lambda(last_row, lambda x: x == 1)
        actions = self.get_legal_actions()
        if self.player_one:
            second_won = second_won or len(actions) == 0
        else:
            first_won = first_won or len(actions) == 0
        return first_won or second_won

    def game_result(self):
        '''
        Modify according to your game or 
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''
        board = self.get_state_board(self.state)
        first_row = board[0]
        last_row = board[2]
        second_won = any_lambda(first_row, lambda x: x == 2)
        first_won = any_lambda(last_row, lambda x: x == 1)
        actions = self.get_legal_actions()
        if self.player_one:
            second_won = second_won or len(actions) == 0
        else:
            first_won = first_won or len(actions) == 0
        if first_won:
            return -1
        else:
            return 1

    def move(self, action):
        player_index = 0 if self.player_one else 1
        opponent_index = 1 if self.player_one else 0
        state = np.copy(self.state)
        player_state = state[player_index]
        opponent_state = state[opponent_index]
        previous_position = action[0]
        new_position = action[1]
        for index, position in enumerate(player_state):
            current_x, current_y = position[0], position[1]
            # If this was the previous position
            if previous_position[0] == current_x and previous_position[1] == current_y:
                # Set the new state
                if new_position[0] != current_x and new_position[1] != current_y:
                    for index_opponent, opponent_position in enumerate(opponent_state):
                        oponnent_current_x, oponnent_current_y = opponent_position[
                            0], opponent_position[1]
                        # If the new position is the one eaten we remove it
                        if new_position[0] == oponnent_current_x and new_position[1] == oponnent_current_y:
                            opponent_state = np.delete(
                                opponent_state, index_opponent
                            )

                player_state[index] = new_position
        state[player_index] = player_state
        state[opponent_index] = opponent_state
        return state
