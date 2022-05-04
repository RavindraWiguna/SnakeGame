class Point:
    def __init__(self, x: int, y:int, last_move) -> None:
        self.x = x
        self.y = y
        # Addition for A*
        self.f = 0
        self.g = 0
        self.h = 0
        self.last_move = None
    
    def __gt__(self, other):
        if(self.f == other.f):
            return self.h > other.h
        return self.f > self.f

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'
    
    def get_state(self):
        return f'{self.x}|{self.y}'# to avoid confusion x=1, y=11, or x=11, y=1