from snakegame.enums import Direction
class Point:
    # DIRECTION_STATE = {Direction.UP.value: 'U', Direction.DOWN.value:'D', Direction.LEFT.value:'L', Direction.RIGHT.value:'R', Direction.NaN.value: 'N'}
    def __init__(self, x: int, y:int, last_move=Direction.NaN) -> None:
        self.x = x
        self.y = y
        # Addition for A*
        self.f = 0
        self.g = 0
        self.h = 0
        self.last_move = last_move
    
    def __gt__(self, other):
        if(self.f == other.f):
            return self.h > other.h
        return self.f > self.f

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y}) | ({self.g}+{self.h}={self.f}) | {self.last_move.name}'
    
    def __repr__(self) -> str:
        return f'({self.x}, {self.y}) | {self.last_move.name}'
    
    def get_state(self):
        # print(self.last_move)
        return f'{self.x}|{self.y}|{self.last_move.name}'# to avoid confusion x=1, y=11, or x=11, y=1