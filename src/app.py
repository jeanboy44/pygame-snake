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

        self.head_up = pygame.image.load("resources/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("resources/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("resources/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("resources/head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("resources/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("resources/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("resources/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("resources/tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load(
            "resources/body_vertical.png"
        ).convert_alpha()
        self.body_horizontal = pygame.image.load(
            "resources/body_horizontal.png"
        ).convert_alpha()

        self.body_tr = pygame.image.load("resources/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("resources/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("resources/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("resources/body_bl.png").convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        """draws snake on grid"""
        for index, block in enumerate(self.body):
            # 1. we still need a rect for the positioning
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # 2.2 what direction is the face heading
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (
                        previous_block.y == -1 and next_block.x == -1
                    ):
                        screen.blit(self.body_tl, block_rect)
                    if (previous_block.x == -1 and next_block.y == 1) or (
                        previous_block.y == 1 and next_block.x == -1
                    ):
                        screen.blit(self.body_bl, block_rect)
                    if (previous_block.x == 1 and next_block.y == -1) or (
                        previous_block.y == -1 and next_block.x == 1
                    ):
                        screen.blit(self.body_tr, block_rect)
                    if (previous_block.x == 1 and next_block.y == 1) or (
                        previous_block.y == 1 and next_block.x == 1
                    ):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        """updates head graphics to the right direction"""
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        """updates tail graphics to the right direction"""
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

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
        self.draw_grass()
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

    def draw_grass(self):
        """draw grass on the grid"""
        grass_color = (167, 209, 61)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load("resources/apple.png").convert_alpha()

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
