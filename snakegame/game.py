from typing import Tuple
import cv2
import pygame
from random import randint, choice
from .snake import Snake
from .food import Food
from .enums import Actions, Direction
from collections import Counter
import numpy as np

# Initialize the pygame
pygame.init()

# Contain the reward, game_over, and score of the game, and just_eat_food
class GameInformation:
    def __init__(self, reward, game_over, score, just_eat_food) -> None:
        self.reward = reward
        self.game_over = game_over
        self.score = score
        self.just_eat_food = just_eat_food


class Game:
    SCORE_FONT = pygame.font.SysFont('comicsans', 50)
    RELATIVE_DIRECTION = {(Direction.UP, Actions.LEFT): Direction.LEFT, 
                          (Direction.UP, Actions.RIGHT): Direction.RIGHT,
                          (Direction.LEFT, Actions.LEFT): Direction.DOWN,
                          (Direction.LEFT, Actions.RIGHT): Direction.UP,
                          (Direction.RIGHT, Actions.LEFT): Direction.UP,
                          (Direction.RIGHT, Actions.RIGHT): Direction.DOWN,
                          (Direction.DOWN, Actions.LEFT): Direction.RIGHT,
                          (Direction.DOWN, Actions.RIGHT): Direction.LEFT}
    def __init__(self, window, width, height, block_size) -> None:
        self.window = window
        self.width = width
        self.height = height
        self.block_size = block_size
        self.total_col = width // block_size
        self.total_row = height // block_size
        self.total_tiles = self.total_col * self.total_row
        if(width % block_size != 0 or height%block_size != 0):
            raise ValueError(f'{block_size} is not the factor of game dimensions ({width} x {height})')

        # Create snake
        self.snake = Snake(self.total_col//2, self.total_row//2, block_size)
        # self.snake.direction = choice((Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP))
        for _ in range(0):
            self.snake.add_body()
        # Create food
        self.food = Food(randint(0, self.total_col-1), randint(0, self.total_row-1), self.block_size)
        self.just_eat_food = False

        # Create score
        self.score = 0
        # Create reward
        self.reward = 0
        # To Store all spawnable tile
        self.spawnable_tiles = []
        # Boolean indicating game over or all tile have been covered
        self.isEnd = False
    
    def _get_spawnable(self):
        self.spawnable_tiles.clear()
        occupied_tiles = Counter()
        for i in range(self.snake.length):
            # Convert snake pos x, y into one single number (sadly non snakin)
            cur_id = self.snake.bodies[i].x + self.snake.bodies[i].y * self.total_col
            # Flag this tile as occupied
            occupied_tiles[cur_id] = 1
        
        # Iterate over all the tiles number
        for i in range(self.total_tiles):
            if(occupied_tiles[i] == 0):
                # add i to list of spawnable tiles if it aint occupied
                self.spawnable_tiles.append(i)

    def _respawn_food(self):
        # Get all possible tile to spawn food
        self._get_spawnable()
        # If there exist a tile to spawn
        if(self.spawnable_tiles):
            self.food.respawn(self.spawnable_tiles, self.total_col)
        else:
            self.isEnd = True

    def _food_collider(self):
        if(abs(self.snake.bodies[0].x - self.food.pos.x) < 1
            and abs(self.snake.bodies[0].y - self.food.pos.y)< 1):
           
            self.score+=1
            self.reward +=75
            print("uncomment add body to add body")
            # self.snake.add_body()
            self._respawn_food()
            self.just_eat_food = True


    def _wall_collider(self):
        if(self.snake.bodies[0].x >= self.total_col or 
           self.snake.bodies[0].x < 0 or 
           self.snake.bodies[0].y >= self.total_row or 
           self.snake.bodies[0].y < 0):
            self.isEnd = True
            self.reward -=25

    def _snake_collider(self):
        if(self.snake.bodies[0] in self.snake.bodies[1:]):
            self.isEnd = True
            self.reward -= 25

    def _collision_handler(self):
        self._food_collider()
        self._wall_collider()
        self._snake_collider()
        
    def _snake_direction_handler(self, direction: Direction):
        if(abs(direction.value - self.snake.direction.value) > 1):
            self.snake.direction = direction
            self.reward += 5
            print("dir change")
        else:
            # can not change, bad input punish sir (harder than die hahaha)
            self.reward -= 50
            print("dir not")
        # self.snake.direction = direction

    def human_move(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_UP]):
            # print("up")
            self._snake_direction_handler(Direction.UP)
        elif(keys[pygame.K_DOWN]):
            self._snake_direction_handler(Direction.DOWN)
            # print("down")
        elif(keys[pygame.K_LEFT]):
            self._snake_direction_handler(Direction.LEFT)
            # print("left")
        elif(keys[pygame.K_RIGHT]):
            self._snake_direction_handler(Direction.RIGHT)
            # print("right")
    
    def _draw_score(self):
        score_text = self.SCORE_FONT.render(f'{self.score}', 1, (255, 255, 255))
        self.window.blit(score_text, (0, 0))
    
    def _draw_snake(self):
        self.snake.render(self.window)
    
    def _draw_food(self):
        self.food.render(self.window)
    
    def draw(self):
        # Fill the background color as black
        self.window.fill((64, 64, 64))

        self._draw_food()
        self._draw_snake()
        self._draw_score()
    
    # Method to generate alternative input for neural network
    def mini_vision(self, isShow=False):
        # paint background
        frame = np.full((self.total_row, self.total_col), 0, np.float32)
        # paint snake body
        for i in range(self.snake.length):
            frame[self.snake.bodies[i].y][self.snake.bodies[i].x] = -1
        
        # paint food
        frame[self.food.pos.y][self.food.pos.x] = 1.0
        # paint head bit bigger init
        frame[self.snake.bodies[0].y][self.snake.bodies[0].x] = 0.5
        if(isShow):
            cv2.imshow('test', frame)
            cv2.waitKey(1)
        return frame
    
    # Do a one game loop (move, update, draw)
    def loop(self, isHumanControlled: bool, action):
        """
        Executes a single game loop.
        :returns: GameInformation instance reward, game_over, score.
        """
        if(not self.isEnd):
            self.reward = 0
            self.just_eat_food = False
            if(isHumanControlled):
                # Get human input
                self.human_move()
            else:
                # check is it direction based or action based
                if(isinstance(action, Actions)):
                    if(action != Actions.STRAIGHT):
                        self._snake_direction_handler(self.RELATIVE_DIRECTION[(self.snake.direction, action)])
                else:
                    print(f'snake will move to: {action}')
                    self._snake_direction_handler(action)

            self.snake._move()
            self._collision_handler()
            # print(self.snake.bodies[0].x, self.snake.bodies[0].y)
        
        game_info = GameInformation(self.reward, self.isEnd, self.score, self.just_eat_food)
        
        return game_info
    
    def reset(self):
        self.score = 0
        self.snake.reset()
        self._respawn_food()
        self.isEnd = False
    
    def stop(self):
        cv2.destroyAllWindows()