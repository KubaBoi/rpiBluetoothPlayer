
import json
import pygame

class GUI:
    def __init__(self, screen, bluetoothController):
        self.loadDesign()

        self.bController = bluetoothController
        self.screen = screen
        self.mainFont = pygame.font.SysFont(self.c["fontName"], 30)
        self.smallFont = pygame.font.SysFont(self.c["fontName"], 20)
        self.smallestFont = pygame.font.SysFont(self.c["fontName"], 10)

    def draw(self):
        self.clear()
        self.drawMainButton()
        self.drawNextButton()
        self.drawPrevButton()
        self.drawData()

    def clear(self):
        self.screen.fill(self.c["background"])

    def drawMainButton(self):
        center = self.c["buttonCenter"]
        radius = self.c["buttonRadius"]
        r2 = int(radius/2)
        r6 = int(radius/6)
        r10 = int(radius/10)

        pygame.draw.circle(self.screen, self.c["mainButtonColor1"], center, radius)
        try:
            status = self.bController.data["Status"]
        except:
            status = None

        if (status == None or status == "paused"): # sipka
            pygame.draw.polygon(self.screen, self.c["mainButtonColor2"],
                [
                    (center[0] - r2 + r10, center[1] - r2),
                    (center[0] - r2 + r10, center[1] + r2),
                    (center[0] + r2 + r10, center[1])
                ]
            )
        else: # dve cary
            pygame.draw.polygon(self.screen, self.c["mainButtonColor2"],
                [
                    (center[0] - r2, center[1] - r2),
                    (center[0] - r2 + r6, center[1] - r2),
                    (center[0] - r2 + r6, center[1] + r2),
                    (center[0] - r2, center[1] + r2),
                ]
            )
            pygame.draw.polygon(self.screen, self.c["mainButtonColor2"],
                [
                    (center[0] + r2 - r6/2, center[1] + r2),
                    (center[0] + r2 - r6 - r6/2, center[1] + r2),
                    (center[0] + r2 - r6 - r6/2, center[1] - r2),
                    (center[0] + r2 - r6/2, center[1] - r2),
                ]
            )

    def drawNextButton(self):
        center = self.c["buttonCenter"]
        radius = self.c["buttonRadius"]
        r3 = int(radius/3)

        pygame.draw.polygon(self.screen, self.c["nextButtonColor"],
            [
                (center[0] + radius + r3, center[1] - r3),
                (center[0] + radius + r3, center[1] + r3),
                (center[0] + radius + 3*r3, center[1])
            ]
        )

    def drawPrevButton(self):
        center = self.c["buttonCenter"]
        radius = self.c["buttonRadius"]
        r3 = int(radius/3)

        pygame.draw.polygon(self.screen, self.c["nextButtonColor"],
            [
                (center[0] - radius - r3, center[1] - r3),
                (center[0] - radius - r3, center[1] + r3),
                (center[0] - radius - 3*r3, center[1])
            ]
        )

    def drawData(self):
        try:
            track = self.bController.data["Track"]
            self.writeText(track["Title"], self.mainFont, (0,310), self.c["titleColor"])
            self.writeText(track["Artist"], self.smallFont, (0, 345), self.c["artistColor"])
            self.writeText(track["Album"], self.smallFont, (0, 370), self.c["albumColor"])
        except:
            self.writeText("Title", self.mainFont, (0,310), self.c["titleColor"])
            self.writeText("Artist", self.smallFont, (0, 345), self.c["artistColor"])
            self.writeText("Album", self.smallFont, (0, 370), self.c["albumColor"])

    def writeText(self, text, font, position, color, bold=True):
        textsurface = font.render(text, bold, color)
        self.screen.blit(textsurface, position)

    def loadDesign(self):
        with open("designConfig.json", "r") as f:
            self.c = json.loads(f.read())