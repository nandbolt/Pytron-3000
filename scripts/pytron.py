import pygame
import math
import random
from pygame.math import Vector2

from scripts.pytron_body import PytronBody
from scripts.controller import NPCController
from scripts.particle import Particle

class Pytron:


    def __init__(self, game, x, y, segments=2):
        self.game = game
        self.controller = NPCController(game, self)

        self.head = PytronBody(game, x, y, self, 'head')
        previous_part = self.head
        for i in range(segments - 1):
            part = PytronBody(game, x, y, self, 'body')
            previous_part.previous_part = part
            part.next_part = previous_part
            previous_part = part
        
        self.state = 'normal'
        self.state_timer = 0

        self.time_to_eat = 30
        self.time_to_lunge = 60
    

    def update(self):
        if self.head == None:
            if self in self.game.entities:
                self.game.entities.remove(self)
            return
        
        self.controller.update()
        self.update_state()


    def draw(self, surface):
        pass
    

    def move(self, move_input, move_strength):
        match self.state:
            case 'coiled':
                move_strength *= 0.25
            case 'lunging':
                move_strength *= 1.5
            case 'eating':
                move_strength *= 0.75
            case _:
                pass
        self.head.set_drive_force(move_input, move_strength)


    def change_state(self, new_state):
        if self.state == new_state:
            return
        self.exit_state()
        self.state = new_state
        self.enter_state()


    def enter_state(self):
        match self.state:
            case 'coiled':
                pass
            case 'lunging':
                pass
            case 'eating':
                self.eat_timer = self.time_to_eat
                
                splatter_index = random.randint(1, 3)
                self.game.decals.blit(self.game.assets[f'decal-blood-splatter-{splatter_index}'], self.head.position)
            case _:
                pass
        self.head.change_head_type(self.state)
        self.state_timer = 0
    

    def exit_state(self):
        match self.state:
            case 'coiled':
                pass
            case 'lunging':
                pass
            case 'eating':
                pass
            case _:
                pass


    def update_state(self):
        self.state_timer += 1
        match self.state:
            case 'coiled':
                if self.controller.bite_input == False:
                    self.change_state('lunging')
            case 'lunging':
                if self.state_timer >= self.time_to_lunge:
                    self.change_state('normal')
                else:
                    for entity in self.game.entities:
                        if isinstance(entity, PytronBody) and self != entity.pytron and self.head.collider.colliderect(entity.collider):
                            entity.detach()
                            self.change_state('eating')
                            break
            case 'eating':
                particle = Particle(self.game, self.head.position, 5, 'blood', Vector2(random.randrange(-1, 1), random.randrange(-1, 1)))
                self.game.particles.append(particle)
                if self.state_timer >= self.time_to_eat:
                    self.change_state('normal')
            case _:
                if self.controller.bite_input:
                    self.change_state('coiled')