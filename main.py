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


screen = pygame.display.set_mode((width, height))
color = (255, 255, 255)
screen.fill((color))

pygame.font.init()

running = True

if (not debug):
    bController = BluetoothController()
    thread = threading.Thread(target=bController.serveForever, args=())
    thread.start()
else:
    bController = None

gui = GUI(screen, bController)

while running:

    gui.clear()
    gui.drawMainButton()
    gui.drawData()
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()