import pygame
from pygame.math import Vector2

from scripts.pytron_body import PytronBody
from scripts.controller import NPCController

class Pytron:


    def __init__(self, game, x, y, segments=2):
        self.game = game
        self.controller = NPCController(game, self)

        self.head = PytronBody(game, x, y, 'head')
        previous_part = self.head
        for i in range(segments - 1):
            part = PytronBody(game, x, y, 'body')
            previous_part.previous_part = part
            part.next_part = previous_part
            previous_part = part
        self.move_input = Vector2()
    

    def update(self):
        if self.head == None:
            if self in self.game.entities:
                self.game.entities.remove(self)
            return
        
        self.controller.update()


    def draw(self, surface):
        pass