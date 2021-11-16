import numpy as np

from Hexapawn import Hexapawn


if __name__=="__main__":
    game = Hexapawn(init_state=np.array([
        [(0,0), (1,0), (2,0)],
        [(0,2), (1,2), (2,2)]
    ]))

print(game.get_state_board(game.curr_node.state))
print("Menu")
