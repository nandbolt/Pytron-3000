import sys
import pygame
import random
from pygame.math import Vector2

from scripts.utils import load_image
from scripts.pytron import Pytron
from scripts.meteor import Meteor
from scripts.controller import PlayerController, NPCController

class Game:
    def __init__(self):
        # Pygame
        pygame.init()
        pygame.display.set_caption('Pytron3000')
        self.clock = pygame.time.Clock()

        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont('freesanbold.ttf', 50)
        self.minifont = pygame.font.SysFont('freesanbold.ttf', 30)

        # Room
        self.room_width = 640
        self.room_height = 360
        self.room = pygame.Surface((self.room_width, self.room_height))
        self.decals = pygame.Surface((self.room_width, self.room_height))
        self.decals.set_colorkey((0, 0, 0))

        # Screen
        self.screen = pygame.display.set_mode((1280, 720))

        # Assets
        self.assets = {
            'background-1' : load_image('background/background-1.png'),
            'pytron-head-0' : load_image('pytron/heads/pytron_head-0_0.png'),
            'pytron-head-0-bite-start' : load_image('pytron/heads/pytron_head-0_1.png'),
            'pytron-head-0-bite' : load_image('pytron/heads/pytron_head-0_2.png'),
            'pytron-body-0' : load_image('pytron/bodies/pytron_body-0_0.png'),
            'pytron-head-1' : load_image('pytron/heads/pytron_head-1_0.png'),
            'pytron-head-1-bite-start' : load_image('pytron/heads/pytron_head-1_1.png'),
            'pytron-head-1-bite' : load_image('pytron/heads/pytron_head-1_2.png'),
            'pytron-body-1' : load_image('pytron/bodies/pytron_body-1_0.png'),
            'particle-blood' : load_image('particle/particle-blood.png'),
            'decal-blood-splatter-1' : load_image('decal/decal-blood-splatter-1.png'),
            'decal-blood-splatter-2' : load_image('decal/decal-blood-splatter-2.png'),
            'decal-blood-splatter-3' : load_image('decal/decal-blood-splatter-3.png'),
            'decal-trail-1' : load_image('decal/decal-trail-1.png'),
            'decal-trail-2' : load_image('decal/decal-trail-2.png'),
            'decal-trail-3' : load_image('decal/decal-trail-3.png'),
            'meteor-0' : load_image('meteor/meteor_0.png'),
            'meteor-1' : load_image('meteor/meteor_1.png'),
        }
        self.background_image = self.assets['background-1']

        # Inputs
        self.input_right = False
        self.input_left = False
        self.input_down = False
        self.input_up = False
        self.input_dash = False
        self.input_shoot = False

        # Entities
        self.player = None
        self.entities = []
        self.particles = []

        # GUI
        self.display_message = ""
        self.score = 0
        self.high_score = 0

        # States
        self.main_menu = True
        self.game_ended = False

        # Spawner
        self.spawn_timer = 0
        self.time_to_spawn = 10 * 60
    
    def run(self):
        while True:
            # Check player
            if not self.game_ended and self.player != None and self.player.state == 'eaten':
                self.end_game()

            if not self.main_menu and not self.game_ended:
                self.spawn_timer += 1
                if self.spawn_timer >= self.time_to_spawn:
                    meteors = random.randint(1, 3)
                    for i in range(meteors):
                        self.spawn_meteor()
                    self.spawn_timer = 0
                    self.time_to_spawn = (random.randint(0, 2) * 5 + 10) * 60

            # Update entities
            for entity in self.entities:
                entity.update()

            # Render
            self.room.fill((0, 0, 0))
            self.room.blit(self.background_image, (0, 0))
            self.room.blit(self.decals, (0, 0))
            for entity in self.entities:
                entity.draw(self.room)
            for particle in self.particles.copy():
                kill = particle.update()
                particle.draw(self.room)
                if kill:
                    self.particles.remove(particle)
            if self.main_menu:
                self.room.blit(self.font.render('Pytron3000\n\n(awsd) move     (space) lunge\n\npress space to start', True, (255, 255, 255)), (100, 100))
            if self.game_ended:
                self.room.blit(self.font.render(self.message, True, (255, 255, 255)), (100, 100))
            else:
                self.room.blit(self.minifont.render(str(self.score), True, (255, 255, 255)), (10, 330))
                high_score_text = "H:"
                if self.high_score > 0:
                    high_score_text += str(self.high_score)
                else:
                    high_score_text += 'NONE'
                self.room.blit(self.minifont.render(high_score_text, True, (255, 125, 0)), (300, 330))
            self.screen.blit(pygame.transform.scale(self.room, self.screen.get_size()))

            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.input_right = True
                    if event.key == pygame.K_a:
                        self.input_left = True
                    if event.key == pygame.K_s:
                        self.input_down = True
                    if event.key == pygame.K_w:
                        self.input_up = True
                    if event.key == pygame.K_SPACE:
                        self.input_dash = True
                    if event.key == pygame.K_j:
                        self.input_shoot = True
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    if event.key == pygame.K_p:
                        self.restart()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.input_right = False
                    if event.key == pygame.K_a:
                        self.input_left = False
                    if event.key == pygame.K_s:
                        self.input_down = False
                    if event.key == pygame.K_w:
                        self.input_up = False
                    if event.key == pygame.K_SPACE:
                        self.input_dash = False
                        if self.main_menu:
                            self.start()
                    if event.key == pygame.K_j:
                        self.input_shoot = False

            # Pygame
            pygame.display.update()
            self.clock.tick(60)

            # Debug
            #print(len(self.entities))



    def restart(self):
        self.player = None
        self.entities = []
        self.game_ended = False
        self.message = ''
        self.score = 0

        self.start()


    def start(self):
        self.main_menu = False
        self.player = Pytron(self, self.room.get_width() * 0.5, self.room.get_height(), 2)
        self.player.controller = PlayerController(self, self.player)
        self.player.set_body_variant(0)
        self.entities.append(self.player)
        for i in range(10):
            self.spawn_meteor()


    def spawn_meteor(self):
        x = random.randrange(0, self.room.get_width())
        y = random.randrange(0, self.room.get_height())
        meteor = Meteor(self, x, y)
        self.entities.append(meteor)


    def spawn_npc_snake(self):
        x = random.randrange(0, self.room.get_width())
        y = random.randrange(0, self.room.get_height())
        self.spawn_npc_snake_at(x, y)
    

    def spawn_npc_snake_at(self, x, y):
        segments = random.randint(2, 5)
        snake = Pytron(self, x, y, segments)
        self.entities.append(snake)
    

    def end_game(self):
        self.game_ended = True
        high_score_text = ''
        if self.score > self.high_score:
            self.high_score = self.score
            high_score_text = '(new high)'

        messages = [
            'eaten...',
            'devoured...',
            'consumed...',
        ]
        self.message = messages[random.randint(0, len(messages) - 1)] + f'\n\nate {self.score}{high_score_text}\n\n(p) restart'

def main():
    Game().run()

if __name__ == '__main__':
    main()