#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# The Conway's Game of Life Breeder automaton
# Rules:
# 1. Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
# 2. Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
# 3. Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
# 4. Any dead cell with exactly 3 live neighbors becomes alive, by reproduction

import pandas as pd
import random

LIVE_CHANCE = 0.3
CELL_CHAR = '❤' # replacements u■u▉u▇u▆a❤
CONVERGENCE_LIMIT = 10
# wide populaton range causes ageing and stalemate
# less revive limit brings changing and vitality
MIN_POPULATION = 2
MAX_POPULATION = 3
REVIVE_LIMIT = 3

class CellBoard:
    
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        df = pd.DataFrame(index=range(height), columns=range(width))
        self.df = df.fillna(0)
        self.cells = 0   # all lived cells count
        self.times = 0   # Iterate times
        self.equalized = 0   # board convergence count
        self.convergence = (False, 0)   # is convergenced and convergence times

    @classmethod
    def from_file(cls, file: str):
        with open(file, 'r') as f:
            rows = f.read().split('\n')
        if not rows:
            raise ValueError('Empty File!')

        cb = cls(len(rows[0]), len(rows))
        for i, row in enumerate(rows):
            cb.df.loc[i] = [int(num) for num in row]
        cb.cells = cb.live_count()
        return cb

    def random_state(self):
        self.df = self.df.applymap(lambda x: 0 if random.random() > LIVE_CHANCE else 1)
        self.cells = self.live_count()

    def next_state(self):
        # build neighbor bitmap
        def judge(liveness: int, neighbors: int):
            if liveness:
                if neighbors < MIN_POPULATION or neighbors > MAX_POPULATION:
                    return 0
                return 1
            else:
                if neighbors == REVIVE_LIMIT:
                    return 1
                return 0
        
        pre_cells = self.live_count()
        self.cells = 0
        ndf = self.df.copy()
        for idx in range(self.height):
            for col in range(self.width):
                val = judge(self.df.at[idx, col], self._count_neighbors(idx, col))
                ndf.at[idx, col] = val
                self.cells += val
        self.df = ndf
        # save process record
        self.times += 1
        if self.convergence[0]:
            return
        if pre_cells == self.cells:
            self.equalized += 1
            if self.equalized == CONVERGENCE_LIMIT:
                self.convergence = (True, self.times - CONVERGENCE_LIMIT)
        else:
            self.equalized = 0

    def _count_neighbors(self, idx: int, col: int):
        # use sum to count live cells
        sidx, eidx = max(idx - 1, 0), min(idx + 1, self.height - 1)
        scol, ecol = max(col - 1, 0), min(col + 1, self.width - 1)
        return self.df.loc[sidx:eidx, scol:ecol].to_numpy().sum() - self.df.at[idx, col]
    
    def live_count(self):
        return self.cells or self.df.to_numpy().sum()
    
    def render(self):
        rage = '-' * (len(self.df.columns)*2 + 3)
        print(rage)
        for _, row in self.df.iterrows():
            print('|', *[CELL_CHAR if val else ' ' for val in row], '|', sep=' ')
        print(rage)
        print('\n', repr(self))
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(width={self.width}, height={self.height}, cells(live)={self.live_count()})'


def main():
    import time
    import os
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--width', default=10, type=int, required=False)
    parser.add_argument('-l', '--height', default=10, type=int, required=False)
    parser.add_argument('-f', '--file', type=str, required=False, help='from an init state file')
    parser.add_argument('-t', '--times', type=int, required=False, help='max run times')
    parser.add_argument('-i', '--interval', default=0.5, type=float, required=False, help='interval seconds to flush state')
    args = parser.parse_args()

    if not args.file:
        board = CellBoard(args.width, args.height)
        board.random_state()
    else:
        board = CellBoard.from_file(args.file)

    while True:
        board.render()
        time.sleep(args.interval)
        # input()
        board.next_state()
        convergenced, generation = board.convergence
        if convergenced:
            print(f'CellBoard convergenced, from generation {generation}')
            break
        if board.live_count() == 0 or (args.times and board.times == args.times):
            print(f'Life generation {generation} exceed...Ready to exit...')
            time.sleep(5)
            break
        os.system('clear')


if __name__ == '__main__':
    main()
    