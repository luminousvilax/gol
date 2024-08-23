## Little practise of the game of life

> The Conway's Game of Life Breeder automaton

  Rules:
  1. Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
  2. Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
  3. Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
  4. Any dead cell with exactly 3 live neighbors becomes alive, by reproduction


### Install

```bash
git clone 
pip install ./gol
```

### Usage

```bash
python -m gol [-h] [-w WIDTH] [-l HEIGHT] [-f FILE] [-t TIMES] [-i INTERVAL] [-k] [-r]

optional arguments:
  -h, --help            show this help message and exit
  -w WIDTH, --width WIDTH
  -l HEIGHT, --height HEIGHT
  -f FILE, --file FILE  from an init state file
  -t TIMES, --times TIMES
                        max run times
  -i INTERVAL, --interval INTERVAL
                        interval seconds to flush state
  -k, --killer          put a kiiler cell
  -r, --healer          put a healer cell
```
