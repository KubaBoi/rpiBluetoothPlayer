
import pygame

class GUI:
    def __init__(self, screen, bluetoothController):
        self.backGround = (255, 255, 255)
        self.bController = bluetoothController
        self.screen = screen
        fontName = ""
        self.mainFont = pygame.font.SysFont('Arial', 30)
        self.smallFont = pygame.font.SysFont('Arial', 20)
        self.smallestFont = pygame.font.SysFont('Arial', 10)

    def clear(self):
        pygame.fill(self.backGround)

    def drawMainButton(self):
        pygame.draw.circle(self.screen, (0,0,255), (240, 200), 100)
        pygame.draw.polygon(self.screen, (255,0,0), [(0,0), (20, 20), (20, 0)])

    def drawData(self):
        try:
            track = self.bController.data["Track"]
            self.writeText(track["Title"], self.mainFont, (0,310), (0,255,0))
            self.writeText(track["Artist"], self.smallFont, (0, 345), (0,255,0))
            self.writeText(track["Album"], self.smallFont, (0, 370), (0,255,0))
        except:
            self.writeText("Title", self.mainFont, (0,310), (0,255,0))
            self.writeText("Artist", self.smallFont, (0, 345), (0,255,0))
            self.writeText("Album", self.smallFont, (0, 370), (0,255,0))

    def writeText(self, text, font, position, color):
        textsurface = font.render(text, False, color)
        self.screen.blit(textsurface, position)