from pygame.math import Vector2

class Meteor:
    

    def __init__(self, game, x, y, lifetime=120):
        self.game = game
        self.position = Vector2(x, y)
        self.starting_lifetime = lifetime
        self.lifetime = lifetime
        self.image = self.game.assets['meteor-0']

        self.game.entities.append(self)


    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.game.spawn_npc_snake_at(self.position.x, self.position.y)
            self.game.entities.remove(self)
        elif self.lifetime == 60:
            self.image = self.game.assets['meteor-1']


    def draw(self, surface):
        surface.blit(self.image, self.position)