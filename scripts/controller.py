import random
from pygame.math import Vector2

class Controller:


    def __init__(self, game, pytron):
        self.game = game
        self.pytron = pytron
        self.move_input = Vector2()
        self.bite_input = False
        self.shoot_input = False
        self.drive_strength = 12


    def update(self):
        pass


class PlayerController(Controller):
    
    
    def update(self):
        self.move_input.x = self.game.input_right - self.game.input_left
        self.move_input.y = self.game.input_down - self.game.input_up
        if self.move_input.length() != 0:
            self.move_input.normalize()
        self.bite_input = self.game.input_dash
        self.pytron.move(self.move_input, self.drive_strength)


class NPCController(Controller):


    def __init__(self, game, pytron):
        Controller.__init__(self, game, pytron)
        self.time_to_think = 30
        self.think_timer = 0


    def update(self):
        self.think_timer += 1
        if self.think_timer >= self.time_to_think:
            self.think()
    

    def think(self):
        self.move_input.x = random.randint(-1, 1)
        self.move_input.y = random.randint(-1, 1)
        if self.move_input.length() != 0:
            self.move_input.normalize()
        self.pytron.move(self.move_input, self.drive_strength)

        if self.pytron.state == 'coiled':
            self.bite_input = False
        else:
            self.bite_input = random.randint(0, 2) == 0
        
        self.think_timer = 0