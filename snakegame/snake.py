from pygame import draw
from .point import Point
from .enums import Direction


class Snake:
    '''
    Takes 3 arguments (x: int, y:int, size:int)\n
    x, y are the index of the tile, where the head of the snake be\n
    size is the size of the tile (square)\n
    example: Snake(1, 2, 10) will create the snake on (10, 20) pixel coordinate with dimmension ( 10 x 10 )
    '''
    INNER_COLOR = (51, 255, 51) # Green
    OUTER_COLOR = (10, 235, 10) # Green too

    def __init__(self, x:int, y:int, block_size:int) -> None:
        self.size = block_size
        self.inner_size = self.size//2
        self.offset = self.size//4
        self.bodies = [Point(x, y, None)]
        self.length = 1
        self.direction = Direction.RIGHT

        self.init_x = x
        self.init_y = y
    
    def _move(self):
        # it will just loop from bottom to head -1, and if there is new body
        # this is where the last body will get the correct position (automatically)
        for i in range(self.length-1, 0, -1):
            self.bodies[i].x = self.bodies[i-1].x
            self.bodies[i].y = self.bodies[i-1].y
        # Up date head
        if(self.direction == Direction.RIGHT):
            self.bodies[0].x += 1
        elif(self.direction == Direction.LEFT):
            self.bodies[0].x -= 1
        elif(self.direction == Direction.UP):
            self.bodies[0].y -= 1
        else:
            # must be down
            self.bodies[0].y += 1
    
    def add_body(self):
        # just append 0, 0 it will then be updated
        self.bodies.append(Point(-1, -1, None))
        self.length +=1
    
    def render(self, win):
        for i in range(self.length):
            # Draw outer rectangle
            draw.rect(win, self.OUTER_COLOR, (self.bodies[i].x*self.size, self.bodies[i].y*self.size, self.size, self.size))
            # Draw inner rectangle
            draw.rect(win, self.INNER_COLOR, (self.bodies[i].x*self.size + self.offset, self.bodies[i].y*self.size + self.offset, self.inner_size, self.inner_size))

    def reset(self):
        # reset body length to one
        self.length = 1
        # Delete all previous body
        self.bodies.clear()
        # Add new body
        self.bodies.append(Point(self.init_x, self.init_y))