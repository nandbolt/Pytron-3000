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
        self.food = None
        previous_part = self.head
        for i in range(segments - 1):
            part = PytronBody(game, x, y, self, 'body')
            previous_part.previous_part = part
            part.next_part = previous_part
            previous_part = part
        
        self.state = 'normal'
        self.state_timer = 0

        self.time_to_eat = 60
        self.time_to_lunge = 20
    

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
            case 'eaten':
                move_strength *= 0.25
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
                splatter_index = random.randint(1, 3)
                self.game.decals.blit(self.game.assets[f'decal-blood-splatter-{splatter_index}'], self.head.position)
            case 'eaten':
                print('ive been eaten!')
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
            case 'eaten':
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
                elif self.head.pytron == self:
                    for entity in self.game.entities:
                        if isinstance(entity, PytronBody) and self != entity.pytron and self.head.collider.colliderect(entity.collider):
                            self.attach_food(entity)
                            self.change_state('eating')
                            break
            case 'eating':
                particle_velocity = Vector2(2, 0)
                particle_velocity = particle_velocity.rotate(random.randrange(360))
                half_width = self.head.image.get_width() * 0.5
                half_height = self.head.image.get_height() * 0.5
                center = Vector2(self.head.position.x + half_width, self.head.position.y + half_height)
                facing = Vector2(self.head.facing_direction.x * half_width, self.head.facing_direction.y * half_height)
                facing.normalize()
                particle = Particle(self.game, center + facing / 8, 5, 'blood', particle_velocity)
                self.game.particles.append(particle)
                
                if self.state_timer >= self.time_to_eat or self.head.next_part == None:
                    if self.head.next_part != None:
                        self.convert_food()
                    self.change_state('normal')
            case 'eaten':
                pass
            case _:
                if self.controller.bite_input:
                    self.change_state('coiled')
    

    def set_body_variant(self, body_variant):
        part = self.head
        while True:
            part.set_body_variant(body_variant)
            part = part.previous_part
            if part == None:
                break
    

    def attach_food(self, food):
        food.detach()
        if food.body_type == 'head':
            food.pytron.change_state('eaten')
        self.head.set_next_part(food)
        food.pytron = self
        self.food = food
    

    def convert_food(self):
        self.food.detach()
        self.head.set_previous_part(self.food)
        self.food = None