import sys
import pygame

def main():
    pygame.init()
    pygame.display.set_caption('Pytron3000')
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()