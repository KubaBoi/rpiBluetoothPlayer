#640 480

import pygame
from test import BluetoothController

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

    bController = BluetoothController()

pygame.quit()