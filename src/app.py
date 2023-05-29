import random
import sys

import pygame
from pygame.math import Vector2


class Snake:
    def __init__(self):
        """Snake

        Attributes:
            body (Vector2): x, y positions of the snake within the grid
            direction (Vector2): the direction of the snake moves. This value is
                updated with user keyboard input(up, down, left, right)
        """
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        """draws snake on grid"""
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        """update body positions"""
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]


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
snake = Snake()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            snake.move_snake()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                snake.direction = Vector2(1, 0)
    screen.fill((175, 215, 70))
    fruit.draw_fruit()
    snake.draw_snake()
    pygame.display.update()
    clock.tick(60)
