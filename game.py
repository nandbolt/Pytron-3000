import sys
import pygame
import random
from pygame.math import Vector2

from scripts.utils import load_image
from scripts.pytron import Pytron
from scripts.controller import PlayerController, NPCController

class Game:
    def __init__(self):
        # Pygame
        pygame.init()
        pygame.display.set_caption('Pytron3000')
        self.clock = pygame.time.Clock()

        # Room
        self.room_width = 640
        self.room_height = 360
        self.room = pygame.Surface((self.room_width, self.room_height))

        # Screen
        self.screen = pygame.display.set_mode((1280, 720))

        # Assets
        self.assets = {
            'background-1' : load_image('background/background-1.png'),
            'pytron-head-1' : load_image('pytron/heads/pytron_head-1_0.png'),
            'pytron-body-1' : load_image('pytron/bodies/pytron_body-1_0.png'),
        }
        self.background_image = self.assets['background-1']

        # Inputs
        self.input_right = False
        self.input_left = False
        self.input_down = False
        self.input_up = False
        self.input_dash = False
        self.input_shoot = False

        # Entities
        self.player = None
        self.entities = []

        self.start()
    
    def run(self):
        while True:
            # Update entities
            for entity in self.entities:
                entity.update()

            # Render
            self.room.fill((0, 0, 0))
            self.room.blit(self.background_image, (0, 0))
            for entity in self.entities:
                entity.draw(self.room)
            self.screen.blit(pygame.transform.scale(self.room, self.screen.get_size()))

            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.input_right = True
                    if event.key == pygame.K_a:
                        self.input_left = True
                    if event.key == pygame.K_s:
                        self.input_down = True
                    if event.key == pygame.K_w:
                        self.input_up = True
                    if event.key == pygame.K_SPACE:
                        self.input_dash = True
                    if event.key == pygame.K_j:
                        self.input_shoot = True
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    if event.key == pygame.K_p:
                        self.restart()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.input_right = False
                    if event.key == pygame.K_a:
                        self.input_left = False
                    if event.key == pygame.K_s:
                        self.input_down = False
                    if event.key == pygame.K_w:
                        self.input_up = False
                    if event.key == pygame.K_SPACE:
                        self.input_dash = False
                    if event.key == pygame.K_j:
                        self.input_shoot = False

            # Pygame
            pygame.display.update()
            self.clock.tick(60)

            # Debug
            #print(len(self.entities))



    def restart(self):
        self.player = None
        self.entities = []

        self.start()


    def start(self):
        self.player = Pytron(self, self.room.get_width() * 0.5, self.room.get_height(), 10)
        self.player.controller = PlayerController(self, self.player)
        self.entities.append(self.player)
        for i in range(10):
            self.spawn_npc_snake()


    def spawn_npc_snake(self):
        x = random.randrange(0, self.room.get_width())
        y = random.randrange(0, self.room.get_height())
        segments = random.randint(2, 5)
        snake = Pytron(self, x, y, segments)
        self.entities.append(snake)

def main():
    Game().run()

if __name__ == '__main__':
    main()