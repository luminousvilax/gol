#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import random
from typing import Callable
from itertools import product
from .board import CellBoard

class HyperCell:

    def __init__(self, cb: CellBoard, x: int=0, y: int=0) -> None:
        """
        Hyper cell will appear in board randomly by default
        """
        self.cb = cb
        self.x = x or (random.randint(0, self.cb.height - 1))
        self.y = y or (random.randint(0, self.cb.width - 1))

    def move(self, action: Callable[[str], None]):
        """
        Hyper cell move to available neighbour randomly,
        try to take action
        """
        direction = set(product((-1, 0, 1), repeat=2))
        direction.remove((0, 0))
        while movement := random.sample(list(direction), 1)[0]:
            direction.remove(movement)
            if (0 <= (x := self.x + movement[0]) < self.cb.height and
                0 <= (y := self.y + movement[1]) < self.cb.width):
                action(self.x, self.y)
                self.x, self.y = x, y
                break

class Killer(HyperCell):

   def move(self):
        super().move(self.cb.kill)

class Healer(HyperCell):

    def move(self):
        super().move(self.cb.heal)
