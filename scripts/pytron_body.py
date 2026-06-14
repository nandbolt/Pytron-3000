import pygame
import math
from pygame.math import Vector2

class PytronBody:


    def __init__(self, game, x, y, pytron, body_type='body'):
        self.game = game
        self.pytron = pytron

        # Physics
        self.position = Vector2(x, y)
        self.velocity = Vector2()
        self.force = Vector2()
        self.imass = 1 / 10
        self.damping = 0.75
        self.next_pull_constant = 0.1
        self.previous_pull_constant = 0.05
        self.rest_length = 12
        self.drive_force = Vector2()

        # Body
        self.body_type = body_type
        self.image = self.game.assets[f'pytron-{body_type}-1']
        self.facing_direction = Vector2(1, 0)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.angular_acceleration = 0.1

        # Collisions
        self.collider = pygame.Rect(self.position.x, self.position.y, self.width, self.height)

        # Parts
        self.next_part = None
        self.previous_part = None

        self.on_body_type_changed()
        game.entities.append(self)
    

    def update(self):
        self.force += self.drive_force
        self.add_spring_forces()

        self.velocity += self.force * self.imass
        self.velocity *= self.damping
        self.position += self.velocity

        self.handle_boundary_collisions()

        self.handle_facing_direction()

        # Collider
        self.collider.left = self.position.x
        self.collider.top = self.position.y
        self.collider.right = self.position.x + self.width
        self.collider.bottom = self.position.y + self.height

        # Eat
        if self.body_type == 'head':
            for entity in self.game.entities:
                if isinstance(entity, PytronBody) and self.pytron != entity.pytron and self.collider.colliderect(entity.collider):
                    entity.detach()

        self.force.x = 0
        self.force.y = 0


    def draw(self, surface):
        if self.previous_part != None:
            return
        part = self
        while True:
            angle = part.facing_direction.angle
            if math.isnan(angle):
                angle = 0
            
            image = pygame.transform.rotate(part.image, -45 - angle)
            surface.blit(image, part.position)

            if part.next_part == None:
                break
            part = part.next_part


    def change_to_head(self):
        if self.body_type == 'head':
            return
        self.body_type = 'head'
        self.on_body_type_changed()
    

    def change_to_body(self):
        if self.body_type == 'body':
            return
        self.body_type = 'body'
        self.on_body_type_changed()
    

    def on_body_type_changed(self):
        self.image = self.game.assets[f'pytron-{self.body_type}-1']


    def set_drive_force(self, move_input, drive_strength):
        self.drive_force.x = move_input.x * drive_strength
        self.drive_force.y = move_input.y * drive_strength


    def add_spring_forces(self):
        if self.next_part != None:
            self.add_spring_force(self.next_part, self.next_pull_constant)
        if self.previous_part != None:
            self.add_spring_force(self.previous_part, self.previous_pull_constant)
    

    def add_spring_force(self, other, k):
        r = Vector2(other.position.x - self.position.x, other.position.y - self.position.y)
        length = r.length()
        if length > self.rest_length:
            # F = -k(x - l)
            length -= self.rest_length
            r.normalize()
            r *= length * k
            self.force += r


    def handle_facing_direction(self):
        direction = Vector2(1, 0)
        if self.next_part == None:
            direction.x = self.drive_force.x
            direction.y = self.drive_force.y
        elif self.previous_part == None:
            direction.x = self.next_part.position.x - self.position.x
            direction.y = self.next_part.position.y - self.position.y
        else:
            direction.x = self.next_part.position.x - self.previous_part.position.x
            direction.y = self.next_part.position.y - self.previous_part.position.y
        if direction.length() != 0:
            direction.normalize()
            self.facing_direction = self.facing_direction.lerp(direction, self.angular_acceleration)


    def handle_boundary_collisions(self):
        x1 = 0
        y1 = 0
        x2 = self.game.room.get_width() - self.width
        y2 = self.game.room.get_height() - self.height

        if self.position.x < x1:
            self.position.x = x1
            self.velocity.x = 0
        elif self.position.x > x2:
            self.position.x = x2
            self.velocity.x = 0
        if self.position.y < y1:
            self.position.y = y1
            self.velocity.y = 0
        elif self.position.y > y2:
            self.position.y = y2
            self.velocity.y = 0


    def detach(self):
        if self.next_part != None:
            self.next_part.previous_part = None
        if self.previous_part != None:
            self.previous_part.next_part = None
        self.next_part = None
        self.previous_part = None
        if self.body_type == 'head':
            self.pytron.head = None