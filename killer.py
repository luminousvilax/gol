#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import random
from itertools import product
from .board import CellBoard

class Killer:
    
    def __init__(self, cb: CellBoard, x: int=0, y: int=0) -> None:
        """
        killer cell will appear in board center by default
        """
        self.cb = cb
        self.x = x or (self.cb.height // 2)
        self.y = y or (self.cb.width // 2)
        
    def move(self):
        """
        killer cell move to available neighbour randomly,
        try to kill them
        """
        direction = set(product((-1, 0, 1), repeat=2))
        direction.remove((0, 0))
        while movement := random.sample(list(direction), 1)[0]:
            direction.remove(movement)
            if (0 <= (x := self.x + movement[0]) < self.cb.height and
                0 <= (y := self.y + movement[1]) < self.cb.width):
                self.x, self.y = x, y
                self.cb.kill(x, y)
                break        
