import time
import os
import argparse
from .board import CellBoard
from .killer import Killer

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--width', default=10, type=int, required=False)
parser.add_argument('-l', '--height', default=10, type=int, required=False)
parser.add_argument('-f', '--file', type=str, required=False, help='from an init state file')
parser.add_argument('-t', '--times', type=int, required=False, help='max run times')
parser.add_argument('-i', '--interval', default=0.5, type=float, required=False, help='interval seconds to flush state')
parser.add_argument('-k', '--killer', type=bool, default=False, help='whether to put a kiiler cell')
args = parser.parse_args()

if not args.file:
    board = CellBoard(args.width, args.height)
    board.random_state()
else:
    board = CellBoard.from_file(args.file)
killer = Killer(board)

while True:
    board.render()
    time.sleep(args.interval)
    # input()
    board.next_state()
    if args.killer:
        killer.move()
    convergenced, generation = board.convergence
    if convergenced:
        print(f'CellBoard convergenced, from generation {generation}')
        break
    if board.live_count() == 0 or (args.times and board.times == args.times):
        print(f'Life generation {generation} exceed...Ready to exit...')
        time.sleep(5)
        break
    os.system('clear')
