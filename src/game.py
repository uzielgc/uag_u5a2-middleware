"""
    Assigment for U5 A2: Plataforma Middleware

    Author: Eloy Uziel García Cisneros (eloy.garcia@edu.uag.mx)

    usage: import game

    REF: https://www.youtube.com/watch?v=-3B1v-K1oXE&t=605s
"""

# Standard imports
import logging
import os

# Third-party
import pygame

# Custom
from network import Network

logging.basicConfig(level='INFO')
LOGGER = logging.getLogger(__name__)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

RIP = pygame.image.load(os.path.join(PROJECT_DIR, 'assets', 'rip.png'))
RIP = pygame.transform.scale(RIP, (50, 50))

class Player():

    def __init__(self, color, id_, rect: pygame.rect.Rect):
        self.rect = rect
        self.velocity = 2
        self.color = color
        self.id_ = id_

    def draw(self, g: pygame.Surface, players):
        for _, player in players.items():
            if player.get('dead'):
                # Draw tombstone if dead.
                g.blit(RIP, (player['rect'].x, player['rect'].y))
            else:
                pygame.draw.rect(g, player['color'] , player['rect'], 0)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.rect.x += self.velocity
        elif dirn == 1:
            self.rect.x -= self.velocity
        elif dirn == 2:
            self.rect.y -= self.velocity
        else:
            self.rect.y += self.velocity

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(**self.net.player_data)
        self.canvas = Canvas(self.width, self.height, "U5A2...")
        self.game_over = False

    def run(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if not self.game_over:

                if keys[pygame.K_RIGHT]:
                    if self.player.rect.x <= self.width - self.player.velocity:
                        self.player.move(0)

                if keys[pygame.K_LEFT]:
                    if self.player.rect.x >= self.player.velocity:
                        self.player.move(1)

                if keys[pygame.K_UP]:
                    if self.player.rect.y >= self.player.velocity:
                        self.player.move(2)

                if keys[pygame.K_DOWN]:
                    if self.player.rect.y <= self.height - self.player.velocity:
                        self.player.move(3)
            else:
                if keys[pygame.K_SPACE]:
                    self.net.client.close()
                    self.net = Network()
                    self.player = Player(**self.net.player_data)
                    self.game_over = False

            # Send Network Stuff
            players_data = self.send_data()
            if players_data[self.player.id_].get('dead'):
                self.game_over = True
                

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas(), players_data)

            if self.game_over:
                self.canvas.draw_text("You're DEAD!, press (SPACE) to reset.", 25, 10, 10)


            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data =  {'x': self.player.rect.x, 'y': self.player.rect.y}
        reply = self.net.send(data)
        return reply




class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
