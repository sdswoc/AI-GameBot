import neat.config
import pygame  # Importing pygame
from pygame import mixer  # importing mixer for music/sound effects
from classes import Player, Wall  # Importing player and wall class
from constants import music_dict,floor_group, TEXT_FONT  # Importing music_dict (contains path of varies sound effects)
from test import *  # Importing All the methods (functions required)
import neat  # For creating our AI
import visualizee
from test import test_ai as tai
from train import train_ai as trai
from playGame import play,print_text

# Initializing pygame and mixer
pygame.init()
mixer.init()
pygame.font.init()



# NEAT configuration
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    if options["test_ai"] == True:
        import pickle
        with open (os.path.join("TrainedModel/Model1","winner_4"),"rb") as f :
            winner = pickle.load(f)
        winner_net = neat.nn.FeedForwardNetwork.create(winner,config)
        while True:
            # global floor_group
            # floor_group = []
            tai(winner_net,15)
    elif options["train_ai"] == True:
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(2))
        winner = p.run(trai, 2000)

        # Storing the neural network
        import pickle
        with open (f"winner_{6}","wb") as f:
            pickle.dump(winner,f)
        print(winner)
        winner_net = neat.nn.FeedForwardNetwork.create(winner,config)
        visualizee.draw_net(config, winner)
        visualizee.plot_stats(stats, ylog=False, view=True)
        visualizee.plot_species(stats, view=True)



def test(configf):
    global options
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, configf)
    options["test_ai"] = True
    options["train_ai"] = False
    run(config_path)

def train(configf):
    global options 
    options["train_ai"] = True
    options["test_ai"] = False
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, configf)
    run(config_path)

def chooseMode():
    global options
    options = {
    "play" : False,
    "train_ai" : False,
    "test_ai" : False
}
    optionsL = ["play","train_ai", "test_ai"]
    screen = pygame.display.set_mode((550,350))
    pygame.display.set_caption("Choose Mode")
    font = TEXT_FONT
    font.bold = True
    font.italic = False
    clock = pygame.time.Clock()
    bg_image = pygame.image.load(os.path.join("sprites","background.jpg"))
    hs_image = pygame.image.load(os.path.join("sprites","homescreen1.png")).convert_alpha()
    hand_img = pygame.image.load(os.path.join("sprites", "hand.png"))
    hand_rect = hand_img.get_rect(center=(550//2 - 230,330//2 - 110))

    index = 0
    options['play'] = True
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                exit()
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_DOWN and index < len(optionsL)- 1 :
                    hand_rect.y += 100
                    options[optionsL[index]] = False
                    options[optionsL[index + 1]] = True
                    index += 1
                elif event.key == pygame.K_UP and index > 0:
                    hand_rect.y -= 100
                    options[optionsL[index - 1]] = True
                    options[optionsL[index]] = False
                    index -= 1
                elif event.key == pygame.K_RETURN:
                    return options

        screen.blit(bg_image,(0,0))
        screen.blit(hs_image,(290,40))
        print_text("Play",pygame.font.Font('fonts/agency_fb.ttf', 80),screen,(150,50))
        print_text("Train",pygame.font.Font('fonts/agency_fb.ttf', 80),screen,(160,150))
        print_text("Test",pygame.font.Font('fonts/agency_fb.ttf', 80),screen,(150,250))
        screen.blit(hand_img,hand_rect)
        pygame.display.update()
        clock.tick(60)





if __name__ == "__main__":
    result = chooseMode()
    if result["play"] : 
        play()
    elif result["train_ai"]:
        train(os.path.join("TrainedModel/Model1","config_winner_4.txt"))
    elif result["test_ai"]:
        test(os.path.join("TrainedModel/Model1","config_winner_4.txt"))
    



