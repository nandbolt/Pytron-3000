import pygame

class Pytron:


    def __init__(self, game, position):
        self.game = game
        self.position = list(position)
        self.velocity = [0, 0]
        self.image = game.assets['pytron-head-1']
    

    def update(self, move_input=(0, 0)):
        self.velocity[0] = move_input[0]
        self.velocity[1] = move_input[1]

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


    def draw(self, surface):
        surface.blit(self.image, self.position)