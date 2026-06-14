import pygame
from pygame.math import Vector2

class PytronBody:


    def __init__(self, game, x, y, body_type=0):
        self.game = game
        self.position = Vector2(x, y)
        self.velocity = Vector2()
        self.move_input = Vector2()
        self.body_type = body_type
        self.image = pygame.transform.scale(self.game.assets['pytron-body-1'], (game.screen_scale * 16, game.screen_scale * 16))
        self.facing_direction = Vector2(1, 0)
        self.width = 16
        self.height = 16

        self.deacceleration = 0.75
    

    def update(self):
        speed = self.velocity.length()
        self.velocity += self.move_input
        self.velocity *= self.deacceleration
        self.position += self.velocity

        self.handle_boundary_bounce()

        if self.move_input.length() != 0:
            self.facing_direction = self.facing_direction.lerp(self.move_input, 0.1)

        self.move_input.x = 0
        self.move_input.y = 0


    def draw(self, surface):
        image = pygame.transform.rotate(self.image, -45 - self.facing_direction.angle)
        surface.blit(image, self.position * self.game.screen_scale)
    

    def set_move_direction(self, move_direction):
        self.move_input.x = move_direction.x
        self.move_input.y = move_direction.y

    def change_to_head(self):
        self.image = pygame.transform.scale(self.game.assets['pytron-head-1'], (self.game.screen_scale * 16, self.game.screen_scale * 16))
    

    def change_to_body(self):
        self.image = pygame.transform.scale(self.game.assets['pytron-body-1'], (self.game.screen_scale * 16, self.game.screen_scale * 16))
    

    def handle_boundary_bounce(self):
        if self.position.x < 0:
            self.position.x *= -1
            self.velocity.x *= -1

            self.facing_direction.x = 1
            self.move_input.x = 1
        elif self.position.x > self.game.screen_base_width - self.width:
            self.position.x = 2 * (self.game.screen_base_width - self.width) - self.position.x
            self.velocity.x *= -1

            self.facing_direction.x = -1
            self.move_input.x = -1
        if self.position.y < 0:
            self.position.y *= -1
            self.velocity.y *= -1

            self.facing_direction.y = 1
            self.move_input.y = 1
        elif self.position.y > self.game.screen_base_height - self.height:
            self.position.y = 2 * (self.game.screen_base_height - self.height) - self.position.y
            self.velocity.y *= -1

            self.facing_direction.y = -1
            self.move_input.y = -1