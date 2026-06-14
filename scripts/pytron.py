import pygame
from pygame.math import Vector2

from scripts.pytron_body import PytronBody

class Pytron:


    def __init__(self, game, x, y, segments=2):
        self.game = game
        self.parts = [0 for i in range(segments)]
        for i in range(len(self.parts)):
            self.parts[i] = PytronBody(game, x, y)
        self.parts[0].change_to_head()
        self.pull_strength = 1
        self.move_input = Vector2()
    

    def update(self):
        part_count = len(self.parts)

        # Head
        if part_count > 0:
            head = self.parts[0]
            head.set_move_direction(self.move_input)
            head.update()

        # Body
        for i in range(1, part_count):
            move_input = [0, 0]

            body = self.parts[i]
            target_part = self.parts[i - 1]
            r = target_part.position - body.position
            distance = r.length()
            if r.length() != 0:
                r.normalize()

            body.set_move_direction(r * distance / 2000)
            body.update()


    def draw(self, surface):
        part_count = len(self.parts)
        for i in range(0, part_count):
            self.parts[part_count - i - 1].draw(surface)
    

    def set_move_direction(self, move_direction):
        self.move_input.x = move_direction.x
        self.move_input.y = move_direction.y