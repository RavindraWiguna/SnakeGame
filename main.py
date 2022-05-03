import pygame
from snakegame import Game
from neatUtils import visualize
import neat
import pickle
import os
from snakegame.enums import Actions
from numpy import argmax
import time
from snakegame.game import GameInformation

# Global variable for windows
width, height = 480, 480
win = pygame.display.set_mode((width, height))

def play_snake(genome, config):
    global win, width, height
    # create the net to play
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    # tuple of act for net
    actions = (Actions.STRAIGHT, Actions.LEFT, Actions.RIGHT)
    
    # create the game
    snake_game = Game(win, width, height, 24)
    # clock = pygame.time.Clock()
    game_info = GameInformation(0, 0, 0, 0)
    isRunning = True
    total_act_after_eat = 0
    while isRunning and total_act_after_eat < 50*snake_game.snake.length:
        # clock.tick(15)
        xi = snake_game.mini_vision(False)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                isRunning = False
                break
        
        output = net.activate(xi.ravel())
        comp_action = argmax(output)
        game_info = snake_game.loop(False, actions[comp_action])
        genome.fitness += game_info.reward - 0.01*(comp_action != 0)
        if(game_info.just_eat_food):
            total_act_after_eat = -1

        total_act_after_eat+=1
        isRunning = isRunning and not game_info.game_over
        snake_game.draw()
        pygame.display.update()
    
    genome.fitness += game_info.score


def eval_genomes(genomes, config):
    global win, width, height
    print("training genomes")
    """
    Run each genome
    """
    for genome_id, genome in genomes:
        genome.fitness = 0
        play_snake(genome, config)
        # print(f'finish train genome: {genome_id}, got: {genome.fitness}')
            

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 301)

    # Save the winner
    with open("best_genome.pickle", "wb") as saver:    
        pickle.dump(winner, saver, pickle.HIGHEST_PROTOCOL)
        print("WINNER IS SAVED on best_genome.pickle")
    
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    
    # Show output of the most fit genome against training data.
    # print('\nOutput:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    # node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    # visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # To load from last check point (in case the training is stopped syre)
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, './neatUtils/config-feedforward')
    run(config_path)