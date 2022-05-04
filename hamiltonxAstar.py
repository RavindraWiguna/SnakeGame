from collections import Counter, defaultdict
from queue import PriorityQueue
import pygame
from snakegame import Game
from snakegame.enums import Direction
from snakegame.point import Point
import numpy as np

def generate_hamilton_down(width, height, block_size):
    if(width % block_size != 0 or height % block_size != 0):
        raise ValueError(f"Width and Height of the window is not a multiple of {block_size}")
    trow = height//block_size
    tcol = width//block_size
    grid = np.zeros((tcol, trow), np.uint8)
    curPos = Point(0, 0)
    hamilton = []
    tileStep = np.zeros(trow*tcol, np.uint16)
    direction = Point(0, 1)
    goUp = False
    goBack = False
    visited = 0
    goalv = trow*tcol
    while visited < goalv:
        curTile= curPos.x + curPos.y * trow
        tileStep[curTile] = visited
        hamilton.append(curTile)
        grid[curPos.y][curPos.x] = 1
        # print(grid)
        if(not goBack):
            if(curPos.y + direction.y == 0):
                # oh no too far, change direction sir
                direction.x = 1
                direction.y = 0
                goUp = False
            elif(curPos.y + direction.y == trow):
                # oh no too far down, change direction again
                direction.x = 1
                direction.y = 0
                goUp = True
            elif(direction.x == 1):
                # so we going right, well, onli once, so go back again syre
                direction.x = 0
                direction.y = 1 - (2 * goUp)
        
        # additional check for go back
        if(direction.x == 1):
            if(curPos.x == tcol -1):
                # if we are in the last column then well go back
                direction.x = 0
                direction.y = -1
                goBack = True
                # print("here", curPos)
        elif(goBack):
            direction.x = -1
            direction.y = 0
            # goBack =False
            # print("not here", curPos)
        
        # update curPos
        curPos.x += direction.x
        curPos.y += direction.y
        visited+=1
        # input("")
    # print(grid)
    # for point in hamilton:
        # print(point)
    # print(Counter(tileStep))
    return hamilton, tileStep

def get_direction(head: Point, nextPoint: Point):
    if(nextPoint.x > head.x):
        return Direction.RIGHT
    if(nextPoint.x < head.x):
        return Direction.LEFT
    if(nextPoint.y > head.y):
        return Direction.DOWN
    return Direction.UP

def get_hamilton_direction(head: Point, trow: int, ttiles:int, hamiltons: list, tileSteps: list):
    curTile = head.x + head.y * trow
    curHamiltonStep = tileSteps[curTile]    # get the ?th step of hamnilton
    nextStep = curHamiltonStep+1
    nextStep = nextStep%(ttiles)
    nextTile = hamiltons[nextStep]
    nextPoint = Point(nextTile%trow, nextTile//trow)
    # print(head, curTile, curHamiltonStep, nextStep, nextTile, nextPoint)
    return get_direction(head, nextPoint)

def get_heuristic_val(p1: Point, p2: Point):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def reconstruct_path(finish_state, cameFrom: dict):
    path = []
    cur_state = finish_state
    while (cur_state):
        cur_state, move = cameFrom[cur_state]
        path.append(move)
    return path[::-1] #reverse the path, and return it

def create_node(min_node: Point, direction: Direction):
    x, y = min_node.x, min_node.y
    if(direction == Direction.UP):
        return Point(x, y-1, direction)
    if(direction == Direction.LEFT):
        return Point(x-1, y, direction)
    if(direction == Direction.DOWN):
        return Point(x, y+1, direction)
    return Point(x + 1, y, direction)

def a_star(start_point: Point, goal_point: Point, tcol: int, trow: int, bodies: list, last_move):
    total_opened_node = 0
    print(start_point, goal_point)
    open_nodes = PriorityQueue()#store node that haven't explored with pqueue
    closed_state = Counter() #counter for state that has been explored
    everInOpen = Counter()
    cameFrom = {} #dict to map where a node came from
    
    #node scores
    gScore = defaultdict(lambda:float('inf'))
    gScore[start_point.get_state()] = 0 #save start node state gscore to 0
    start_point.h = get_heuristic_val(start_point, goal_point) 
    start_point.f = start_point.h
    start_point.last_move = last_move
    open_nodes.put(start_point)
    everInOpen[start_point.get_state()]+=1
    cameFrom[start_point.get_state()] = (None, ".")
    total_opened_node+=1
    path = None #saved path for return value
    tentative_gScore = None #variable to hold min node gScore
    #get all possible move
    possible_move = (Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT)
    # reverse move
    reverse_move = {Direction.UP: Direction.DOWN, Direction.DOWN:Direction.UP, Direction.LEFT:Direction.RIGHT,Direction.RIGHT:Direction.LEFT,None:None}
    #loop while open list is not empty in pythonic way
    while open_nodes:
        #get node with min f value
        min_node = open_nodes.get()
        # print(min_node)
        #add min node counter in 
        closed_state[min_node.get_state()]+=1
        
        #check if it is the goal node
        if (min_node == goal_point):
            # print("HEY, Found the goal!")
            path = reconstruct_path(min_node.get_state(), cameFrom)
            break
        

        # print(f'got {len(possible_move)} possible move')
        for move in possible_move:
            if(move == reverse_move[min_node.last_move]):
                continue
            #generate node based on move
            nextNode = create_node(min_node, move)
            # check wall
            if(nextNode.x >= tcol or nextNode.x < 0 or nextNode.y < 0 or nextNode.y >= trow):
                continue
            # check body
            if(nextNode in bodies):
                continue
            # print(move_state)
            # os.system("pause")
            #check if this node's state has been reached/visited/closed
            if(closed_state[nextNode.get_state()] > 0):
                continue
           
            #this node havent yet visited
            tentative_gScore = gScore[min_node.get_state()] + 1 #distance of node is same, so always +1
            if(tentative_gScore < gScore[nextNode.get_state()]):
                #Found a smaller g score of this state, so update the g score and cameFrom
                cameFrom[nextNode.get_state()] = (min_node.get_state(), move)
                gScore[nextNode.get_state()] = tentative_gScore
                #calculate other value of this node
                nextNode.h = get_heuristic_val(nextNode, goal_point)
                nextNode.f = tentative_gScore + nextNode.h
                
                #check if it is not in the open set
                if(everInOpen[nextNode.get_state()]==0):
                    #never in open
                    total_opened_node+=1
                    open_nodes.put(nextNode)
                    everInOpen[nextNode.get_state()]+=1
                # if(nextNode not in open_nodes.queue):
                    # total_opened_node+=1
                    # open_nodes.put(nextNode)

        #End of For Loop
    #End of While Loop
    # print(path[1])
    # print(path)
    for dir in path:
        print(dir)
    # print("|")
    # input("contiunue")
    return path[1] # this is auto path

def play_snake_a_star():
    width, height = 480, 480
    win = pygame.display.set_mode((width, height))
    snake_game = Game(win, width, height, 24)
    clock = pygame.time.Clock()
    isRunning = True
    direction = snake_game.snake.direction
    last_direction = None
    snake_game.draw()
    pygame.display.update()
    while isRunning:
        clock.tick(25)
        # snake_game.mini_vision(True)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                isRunning = False
                break
        last_direction = direction
        direction = a_star(snake_game.snake.bodies[0], snake_game.food.pos, snake_game.total_col, snake_game.total_row, snake_game.snake.bodies[1:], last_direction)
        game_info = snake_game.loop(False, direction)
        # input("")
        isRunning = isRunning and not game_info.game_over
        snake_game.draw()
        pygame.display.update()
        
    
    snake_game.stop()
    pygame.quit()  


def play_snake():
    width, height = 480, 480
    win = pygame.display.set_mode((width, height))
    snake_game = Game(win, width, height, 24)
    clock = pygame.time.Clock()
    isRunning = True
    hamiltons, tileSteps = generate_hamilton_down(width, height, 24)
    while isRunning:
        clock.tick(25)
        # snake_game.mini_vision(True)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                isRunning = False
                break
        direction = get_hamilton_direction(snake_game.snake.bodies[0], snake_game.total_row, snake_game.total_tiles, hamiltons, tileSteps)
        game_info = snake_game.loop(False, direction)
        isRunning = isRunning and not game_info.game_over
        snake_game.draw()
        
        pygame.display.update()
    
    snake_game.stop()
    pygame.quit()

if __name__ =="__main__":
    # arr = [Point(1, 2), Point(3, 4)]
    # print(arr)
    # print(Point(1, 2))
    # generate_hamilton_down(480, 480, 24)
    # play_snake()
    play_snake_a_star()
