import neat.config
import pygame  # Importing pygame
from pygame import mixer  # importing mixer for music/sound effects
from classes import Player, Wall  # Importing player and wall class
from constants import music_dict  # Importing music_dict (contains path of varies sound effects)
from methods import *  # Importing All the methods (functions required)
import neat  # For creating our AI

# Initializing pygame and mixer
pygame.init()
mixer.init()


# NEAT configuration
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Creating Population -> Generates population based on our config files
    p = neat.Population(config)

    # Configuring stats reporter -> To get detailed statistics about each generation
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # we need give our fitness function to the run function -> main
    winner = p.run(main, 100)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)

# Main Loop

# main()
