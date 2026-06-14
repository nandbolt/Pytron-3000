import pygame
from pygame.math import Vector2

class PytronBody:


    def __init__(self, game, x, y, body_type=0):
        self.game = game
        self.position = Vector2(x, y)
        self.velocity = Vector2()
        self.move_input = Vector2()
        self.body_type = body_type
        self.image = self.game.assets['pytron-body-1']

        self.deacceleration = 0.75
    

    def update(self):
        speed = self.velocity.length()
        self.velocity += self.move_input
        self.velocity *= self.deacceleration
        self.position += self.velocity

        self.move_input.x = 0
        self.move_input.y = 0


    def draw(self, surface):
        surface.blit(self.image, self.position)
    

    def set_move_direction(self, move_direction):
        self.move_input.x = move_direction.x
        self.move_input.y = move_direction.y

    def change_to_head(self):
        self.image = self.game.assets['pytron-head-1']
    

    def change_to_body(self):
        self.image = self.game.assets['pytron-body-1']