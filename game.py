import sys
import pygame

from scripts.utils import load_image
from scripts.pytron import Pytron

class Game:
    def __init__(self):
        # Pygame
        pygame.init()
        pygame.display.set_caption('Pytron3000')
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        # Assets
        self.assets = {
            'pytron-head-1' : load_image('pytron/heads/pytron_head-1_0.png')
        }

        # Inputs
        self.input_right = False
        self.input_left = False
        self.input_down = False
        self.input_up = False

        # Player
        self.player = Pytron(self, (100, 100))
    
    def run(self):
        while True:
            # Update entities
            self.player.update((self.input_right - self.input_left, self.input_down - self.input_up))

            # Render
            self.screen.fill((0, 0, 0))
            self.player.draw(self.screen)

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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.input_right = False
                    if event.key == pygame.K_a:
                        self.input_left = False
                    if event.key == pygame.K_s:
                        self.input_down = False
                    if event.key == pygame.K_w:
                        self.input_up = False

            # Pygame
            pygame.display.update()
            self.clock.tick(60)

def main():
    Game().run()

if __name__ == '__main__':
    main()