import random
import sys

import pygame
from pygame.math import Vector2


class Fruit:
    def __init__(self):
        """Fruit object

        Attributes:
            x (int): x position of the object within the grid
            y (int): y position of the object  within the grid
            pos (Vector2): x, y position of the object within the grid
        """
        self.x: int = random.randint(0, cell_number - 1)  # nosec: B311
        self.y: int = random.randint(0, cell_number - 1)  # nosec: B311
        self.pos: Vector2 = Vector2(self.x, self.y)

    def draw_fruit(self):
        """draws the fruit to the screen"""
        fruit_rect = pygame.Rect(
            self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size
        )
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

fruit = Fruit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((175, 215, 70))
    fruit.draw_fruit()
    pygame.display.update()
    clock.tick(60)
