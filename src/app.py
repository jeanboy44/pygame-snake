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
            new_block (bool): Whether to add a new block or not
        """
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        """draws snake on grid"""
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        """update body positions. If new_block is True, one cell is added to the tail
        of the body"""
        if self.new_block is True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Fruit:
    def __init__(self):
        """Fruit object

        Attributes:
            x (int): x position of the object within the grid
            y (int): y position of the object  within the grid
            pos (Vector2): x, y position of the object within the grid
        """
        self.randomize()

    def draw_fruit(self):
        """draws the fruit to the screen"""
        fruit_rect = pygame.Rect(
            self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size
        )
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        """randomize the position of the fruit"""
        self.x: int = random.randint(0, cell_number - 1)  # nosec: B311
        self.y: int = random.randint(0, cell_number - 1)  # nosec: B311
        self.pos: Vector2 = Vector2(self.x, self.y)


class Main:
    """Main

    Attributes:
        snake (Snake) : snake object
        fruit (Fruit) : fruit object
    """

    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        """update all events on screen"""
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        """draw all events on screen"""
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        """check if the snake eats fruit"""
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        """check if 1. the snake moves to out of the grid, 2. the snake colides with
        the fruit, which are the condtions for game failure"""
        if (not 0 <= self.snake.body[0].x < cell_number) or (
            not 0 <= self.snake.body[0].y < cell_number
        ):
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        """game over"""
        pygame.quit()
        sys.exit()


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load("resources/다운로드.png").convert_alpha()

main_game = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
