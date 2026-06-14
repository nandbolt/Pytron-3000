from pygame.math import Vector2

class Particle:


    def __init__(self, game, position, lifetime, particle_type='blood', velocity=Vector2()):
        self.game = game
        self.position = Vector2(position.x, position.y)
        self.velocity = velocity
        self.lifetime = lifetime
        self.particle_type = particle_type
        self.image = game.assets['particle-' + particle_type]
    

    def update(self):
        kill = False
        if self.lifetime <= 0:
            kill = True
        else:
            self.lifetime -= 1
        
        self.position += self.velocity
        
        return kill


    def draw(self, surface):
        surface.blit(self.image, self.position)