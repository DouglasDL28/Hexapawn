import numpy as np

class Node:
    def __init__(self, state:np.ndarray, parent, action:np.ndarray):
        self.state = state
        self.parent = parent
        self.action = action
