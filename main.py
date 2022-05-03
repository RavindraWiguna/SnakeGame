import pygame
from snakegame import Game

if __name__ =="__main__":
    width, height = 640, 480
    win = pygame.display.set_mode((width, height))
    snake_game = Game(win, width, height, 32)
    clock = pygame.time.Clock()
    isRunning = True
    while isRunning:
        clock.tick(15)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                isRunning = False
                break
        
        game_info = snake_game.loop(True)
        isRunning = isRunning and not game_info.game_over
        snake_game.draw()
        pygame.display.update()
    
    pygame.quit()