from pygame import draw
from .point import Point
from collections import Counter
from random import choice

class Food:
    '''
    Takes 3 argument (x: int, y: int, size: int)\n
    x, y are the index of the tile where the food will spawn\n
    size is the size of the food (square)\n
    example: Food(1, 2, 10) will spawn food at (10, 20) pixel coordinate with dimmension ( 10 x 10 )
    '''
    COLOR = (250, 2, 3)
    def __init__(self, x:int, y:int, size:int) -> None:
        self.pos = Point(x, y)
        self.size = size
    
    def render(self, win):
        draw.rect(win, self.COLOR, (self.pos.x*self.size, self.pos.y*self.size, self.size, self.size))
    
    def respawn(self, spawnable_tiles:list, total_col: int):
        idRespawn = choice(spawnable_tiles)

        # extract row and col from idrespawn
        x, y = idRespawn % total_col, idRespawn // total_col
        self.pos.x = x
        self.pos.y = y