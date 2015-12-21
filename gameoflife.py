# Rules:
# Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by over-population.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
import random, pprint
import sys, time, os
from copy import copy

WIDTH=100
HEIGHT=50
SLEEP=0.2

def print_state(data):
    """
    Print array of data to terminal
    """
    rows = len(data)
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in data:
        sys.stdout.write(''.join(['X' if x else ' ' for x in row]) + '\n')
    sys.stdout.flush()

def generate_initial(xsize,ysize):
    """
    Generate a randomized grid
    """
    res = []
    for y in range(ysize):
        row = []
        for x in range(xsize):
            row.append(random.sample([0]*20 + [1]*2,1)[0])
        res.append(row)
    return res

def get_surrounding(x, y, data):
    '''
    >>> import pprint
    >>> data = [
    ... [0,1,1,1,0],
    ... [1,0,1,0,1],
    ... [0,0,0,0,0],
    ... [0,1,0,0,0],
    ... [1,0,0,0,0]
    ... ]

    >>> pprint.pprint(get_surrounding(0,0, data))
    {'center': 0,
     'east': 0,
     'north': 0,
     'northeast': 0,
     'northwest': 0,
     'south': 1,
     'southeast': 0,
     'southwest': 0,
     'west': 1}
    
    >>> pprint.pprint(get_surrounding(2,2,data))
    {'center': 0,
     'east': 0,
     'north': 1,
     'northeast': 0,
     'northwest': 0,
     'south': 0,
     'southeast': 1,
     'southwest': 0,
     'west': 0}

    >>> pprint.pprint(get_surrounding(4,2,data))
    {'center': 0,
     'east': 0,
     'north': 1,
     'northeast': 0,
     'northwest': 0,
     'south': 0,
     'southeast': 0,
     'southwest': 0,
     'west': 0}
     
    '''
    getters = {
        'center': lambda x,y: (x,y),
        'north': lambda x,y: (x, y-1),
        'south': lambda x,y: (x, y+1),
        'east': lambda x,y: (x-1, y),
        'west': lambda x,y: (x+1, y),
        'northeast': lambda x,y: (x-1, y-1),
        'northwest': lambda x,y: (x+1, y-1),
        'southeast': lambda x,y: (x-1, y+1),
        'southwest': lambda x,y: (x+1, y+1)
    }
    res = {}
    for k, f in getters.items():
        v = 0
        vx, vy = f(x,y)
        if not (vx < 0 or vy < 0):
            try:
                v = data[vy][vx]
            except IndexError:
                pass
        res[k] = v
    return res

def count_live_neighbors(datum):
    count = 0
    for k, v in datum.items():
        if k == 'center':
            continue
        count += v
    return count

def transform(data):
    rdata = []
    for y, row in enumerate(data):
        nrow = []
        for x, cell in enumerate(row):
            v = get_surrounding(x, y, data)
            live_neighbors = count_live_neighbors(v)
            if v['center']:
                if live_neighbors < 2 or live_neighbors > 3:
                    nrow.append(0)
                else:
                    nrow.append(1)
            else:
                if live_neighbors == 3:
                    nrow.append(1)
                else:
                    nrow.append(0)
        rdata.append(nrow)
    return rdata


def main():
    data = generate_initial(WIDTH,HEIGHT)
    while True:
        print_state(data)
        data = transform(data)
        time.sleep(SLEEP)
    
if __name__ == '__main__':
    main()

