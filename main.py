#640 480

import pygame
from pygame.locals import*
import threading

from gui import GUI

debug = False

if (not debug):
    from bluetoothController import BluetoothController

pygame.init()

width = 480
height = 640
if (not debug):
    #full screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((width, height))

color = (255, 255, 255)
screen.fill((color))

running = True

if (not debug):
    bController = BluetoothController()
    thread = threading.Thread(target=bController.serveForever, args=())
    thread.start()

gui = GUI(screen)

while running:

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()