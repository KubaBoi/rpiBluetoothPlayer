#640 480

from typing_extensions import runtime
import pygame

pygame.init()

#full screen
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

width = 480
height = 640
screen = pygame.display.set_mode((width, height))

color = (255, 255, 255)
screen.fill((color))

running = True

while running:
    

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()