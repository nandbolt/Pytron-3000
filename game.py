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
        self.screen_base_width = 640
        self.screen_base_height = 360
        self.screen_scale = 2
        self.screen = pygame.display.set_mode((self.screen_base_width * self.screen_scale, self.screen_base_height * self.screen_scale))
        self.clock = pygame.time.Clock()

        # Assets
        self.assets = {
            'pytron-head-1' : load_image('pytron/heads/pytron_head-1_0.png'),
            'pytron-body-1' : load_image('pytron/bodies/pytron_body-1_0.png'),
        }

        # Inputs
        self.input_right = False
        self.input_left = False
        self.input_down = False
        self.input_up = False
        self.input_dash = False
        self.input_shoot = False

        # Entities
        self.player = None
        self.snakes = []

        self.start()
    
    def run(self):
        while True:
            # Update entities
            for snake in self.snakes:
                snake.update()

            # Render
            self.screen.fill((0, 0, 0))
            for snake in self.snakes:
                snake.draw(self.screen)

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



    def restart(self):
        self.player = None
        self.snakes = []

        self.start()


    def start(self):
        self.player = Pytron(self, self.screen_base_width * 0.5, self.screen_base_height * 0.5, 5)
        self.player.set_controller(PlayerController(self, self.player))
        self.snakes = [self.player]
        for i in range(10):
            self.spawn_npc_snake()


    def spawn_npc_snake(self):
        x = random.randrange(0, self.screen_base_width)
        y = random.randrange(0, self.screen_base_height)
        segments = random.randint(2, 5)
        snake = Pytron(self, x, y, segments)
        snake.set_controller(NPCController(self, snake))
        self.snakes.append(snake)

def main():
    Game().run()

if __name__ == '__main__':
    main()