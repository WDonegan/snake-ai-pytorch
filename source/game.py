import random
from collections import namedtuple
from enum import Enum

import numpy as np
import pygame

pygame.init()
font_score = pygame.font.Font('../fonts/arial.ttf', 24)
font_lrg = pygame.font.Font('../fonts/arial.ttf', 40)
font_sml = pygame.font.Font('../fonts/arial.ttf', 14)
font_tny = pygame.font.Font('../fonts/arial.ttf', 10)
font_tnyblk = pygame.font.Font('../fonts/ariblk.ttf', 10)


# font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
GRAY1 = (172, 172, 172)
GRAY2 = (128, 128, 128)
GRAY3 = (64, 64, 64)
BLACK = (0, 0, 0)
RED1 = (200, 0, 0)
RED2 = (255, 140, 0)
GREEN = (124, 252, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)

BLOCK_SIZE = 20
SPEED = 200

# rewards
HIT_WALL = -9
HIT_SELF = -10
TOO_SLOW = -2
LOOPING = -1
ATE_FOOD = 10


class SnakeGameAI:
    direction: Direction
    head: Point
    food: Point
    snake: []
    score: int
    frame_iterations: int
    plot_data: []
    plot_data_raw: []
    paused: bool
    show_plot: bool
    show_matplot: bool

    def __init__(self, w=1280, h=760):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.plot_surf = pygame.Surface((self.w, self.h))
        self.plot_surf.set_alpha(100)
        self.reset()
        self.show_plot = True
        self.show_matplot = False

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.frame_iterations = 0
        self.paused = False
        self.plot_data = []
        self.plot_data_raw = []
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def read_input(self):
        # 0. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAUSE:
                    self.paused = not self.paused
                if event.key == pygame.K_F1:
                    self.show_plot = not self.show_plot
                if event.key == pygame.K_F2:
                    self.show_matplot = not self.show_matplot
        if self.paused:
            self._update_ui()
        return self.paused, self.show_plot, self.show_matplot

    def play_step(self, action):
        # 1. Start counting frame iterations
        self.frame_iterations += 1

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iterations > 100 * len(self.snake):
            game_over = True
            reward = HIT_WALL
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = ATE_FOOD
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def update_plot_data(self, scores: []):
        self.plot_data_raw = scores
        self.plot_data = scores[-int(self.w / 2):]

    def calc_high_score(self) -> (int, int):
        hs = 0
        idx = 0
        i = 0
        for score in self.plot_data:
            if score >= hs:
                hs = score
                idx = i
            i += 1
        return idx, hs

    def _update_ui(self):
        # Clear screen
        self.display.fill(BLACK)

        # Show Plot
        if self.show_plot:
            self.plot_surf.fill(BLACK)
            hsi, hs = self.calc_high_score()
            high_score = font_tnyblk.render(f'{hs}', True, WHITE)
            iterations = font_tny.render(f'{hsi}/{len(self.plot_data_raw)}', True, WHITE)
            x = 0
            for score in self.plot_data:
                y = self.h - ((score * 2) + 2)
                if score > 0:
                    pygame.draw.line(self.plot_surf, GRAY1, (x, y), (x, self.h))
                    pygame.draw.line(self.plot_surf, GRAY1, (x + 1, y), (x + 1, self.h))
                else:
                    pygame.draw.line(self.plot_surf, GRAY3, (x, self.h - 4), (x, self.h))
                    pygame.draw.line(self.plot_surf, GRAY3, (x + 1, self.h - 4), (x + 1, self.h))
                x += 2

            if hs > 0:
                self._place_text(self.plot_surf, Point(hsi * 2, (self.h - ((hs * 2) + 2)) - 16), high_score)
                self._place_text(self.plot_surf, Point(hsi * 2, (self.h - ((hs * 2) + 2)) - 8), iterations)

            self.display.blit(self.plot_surf, [0, 0])

        # Draw snake
        for pt in self.snake:
            if self.snake.index(pt) == 0:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x + 4, pt.y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8))
                pygame.draw.rect(self.display, BLACK, pygame.Rect(pt.x + 8, pt.y + 8, BLOCK_SIZE - 16, BLOCK_SIZE - 16))
            else:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8))

        # Draw food
        pygame.draw.rect(self.display, RED1, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, RED2, pygame.Rect(self.food.x + 4, self.food.y + 4, BLOCK_SIZE - 9, BLOCK_SIZE - 9))

        # Draw score
        score = font_score.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(score, [2, 0])

        # Draw paused text
        if self.paused:
            above = Point(self.w / 2, (self.h / 2) - 15)
            paused = font_lrg.render("PAUSED", True, WHITE)
            self._place_text(above, paused)

            below = Point(self.w / 2, (self.h / 2) + 15)
            press_to_continue = font_sml.render("Press PAUSE to continue...", True, WHITE)
            self._place_text(below, press_to_continue)

        pygame.display.flip()

    @staticmethod
    def _place_text(surf: pygame.Surface, position: Point, text):
        text_size = text.get_size()
        x = position.x - text_size[0] / 2
        y = position.y - text_size[1] / 2
        surf.blit(text, [x, y])

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
