# Rules:
# Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by over-population.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
import random, pprint
import sys, time, os
from copy import copy
from zope.interface import implements
from .interfaces import IGameOfLifeEngine

WIDTH=100
HEIGHT=50
SLEEP=0.2

class GameOfLife(object):
    implements(IGameOfLifeEngine)

    def __init__(self, initial_state=None):
        self._data = initial_state or []

    def randomize(self, xsize, ysize):
        """
        Generate a randomized grid
        """
        res = []
        for y in range(ysize):
            row = []
            for x in range(xsize):
                row.append(random.sample([0]*20 + [1]*2,1)[0])
            res.append(row)
        self._data = res

    def _get_cell(self, x, y):
        '''
        >>> import pprint
        >>> data = [
        ... [0,1,1,1,0],
        ... [1,0,1,0,1],
        ... [0,0,0,0,0],
        ... [0,1,0,0,0],
        ... [1,0,0,0,0]
        ... ]
   
        >>> gol = GameOfLife(data)
        >>> pprint.pprint(gol._get_cell(0,0))
        {'center': 0,
         'east': 0,
         'live_neighbors': 2,
         'north': 0,
         'northeast': 0,
         'northwest': 0,
         'south': 1,
         'southeast': 0,
         'southwest': 0,
         'west': 1}
        
        >>> pprint.pprint(gol._get_cell(2,2))
        {'center': 0,
         'east': 0,
         'live_neighbors': 2,
         'north': 1,
         'northeast': 0,
         'northwest': 0,
         'south': 0,
         'southeast': 1,
         'southwest': 0,
         'west': 0}
    
        >>> pprint.pprint(gol._get_cell(4,2))
        {'center': 0,
         'east': 0,
         'live_neighbors': 1,
         'north': 1,
         'northeast': 0,
         'northwest': 0,
         'south': 0,
         'southeast': 0,
         'southwest': 0,
         'west': 0}
         
        '''
        getters = {
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
            v = 0 # default to zero
            vx, vy = f(x,y)
            if not (vx < 0 or vy < 0):
                try:
                    v = self._data[vy][vx]
                except IndexError:
                    pass
            res[k] = v

        res['live_neighbors'] = sum(res.values())
        res['center'] = self._data[y][x]
        return res

    def step(self):
        rdata = []
        for y, row in enumerate(self._data):
            nrow = []
            for x, cell in enumerate(row):
                v = self._get_cell(x, y)
                if cell:

                    if v['live_neighbors'] < 2 or v['live_neighbors'] > 3:
                        # Any live cell with fewer than two live neighbours 
                        # dies, as if caused by under-population.
                        # Any live cell with more than three live neighbours
                        # dies, as if by over-population.
                        nrow.append(0)
                    else:
                        # Any live cell with two or three live neighbours lives
                        # on to the next generation.
                        nrow.append(1)
                else:
                    if v['live_neighbors'] == 3:
                        # Any dead cell with exactly three live neighbours
                        # becomes a live cell, as if by reproduction.
                        nrow.append(1)
                    else:
                        nrow.append(0)
            rdata.append(nrow)
        self._data = rdata
    
    def __str__(self):
        res = []
        for row in self._data:
            res.append(''.join(
                ['X' if x else ' ' for x in row]))
        return '\n'.join(res)

def main():
    gol = GameOfLife()
    gol.randomize(WIDTH, HEIGHT)
    while True:
        gol.step()
        print gol
        time.sleep(SLEEP)
    
if __name__ == '__main__':
    main()

